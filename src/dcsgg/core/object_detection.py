import os
import json
import pandas as pd
import torch
from torchvision.ops import box_iou

def write_objects_pddl(objects_type_unique_map, outfile):
    t = "(:objects\n"
    for _obj, _type in objects_type_unique_map.items():
        assert ' ' not in _obj and ' ' not in _type
        t += ' ' * 4 + _obj + ' - ' + _type + '\n'
    t += ')'
    with open(outfile, 'w') as f:
        f.write(t)


class ObjectDetection:
    def __init__(self, model, dataset, dinox_detection_dir, rec_detection_dir, out_dir, verbosity):
        self.model = model
        self.dataset = dataset
        self.dinox_detection_dir=dinox_detection_dir
        self.rec_detection_dir = rec_detection_dir
        self.verbosity = verbosity
        self.pddl_stub_out_dir = out_dir

    def supplemental_object_detection(self, missing_obj_referral_phrases, test_problem_id):
        if len(missing_obj_referral_phrases) > 0:
            image = self.dataset.get_observation(test_problem_id)
            text_missing_phrases = '.'.join([p.replace('_', ' ') for p in missing_obj_referral_phrases]) + '.'
            if self.verbosity > 1: print('detecting the following additional phrases:', text_missing_phrases)
            obj_det_res_additional = self.model.inference_phrasewise(image, text_missing_phrases)
            obj_det_res_additional['labels'] = [l.replace(' ', '_') for l in obj_det_res_additional['labels']]
            return obj_det_res_additional


    # provide regular detections from dino-x (as json file in objdet-out dir, 'labels'=jsondict.keys(), boxes=jsondict.values())
    def load_regular_detections(self, problem_id):
        with open(os.path.join(self.dinox_detection_dir, f'objdet_ex0_test{problem_id}.json')) as f:
            dinox_detections = json.load(f)
        obj_det_res_regular = {'labels': list(dinox_detections.keys()),
                               'boxes': torch.tensor(list(dinox_detections.values()))}

        # objdet_by_type = domain.get_detected_objects_by_types(objdet_res_to_pd(obj_det_res_regular))
        return obj_det_res_regular  # , objdet_by_type

    def write_detections(self, replacement_dict, test_id, example_id):
        with open(os.path.join(self.dinox_detection_dir, f'objdet_ex0_test{test_id}.json'), 'r') as f:
            original_dinox_det = json.load(f)

        renamed_dino_x_det = {}
        for lab in original_dinox_det:
            if lab in replacement_dict:
                # replacement_dict: key:from, value:to
                renamed_dino_x_det[replacement_dict[lab]] = original_dinox_det[lab]
            else:
                renamed_dino_x_det[lab] = original_dinox_det[lab]
        with open(os.path.join(self.rec_detection_dir, f'objdet_ex{example_id}_test{test_id}.json'), 'w') as f:
            json.dump(renamed_dino_x_det, f)

    def write_pddl_object_stubs(self, objects_type_map, test_id, example_id):
        e, t = example_id, test_id
        write_objects_pddl(objects_type_map,
                           os.path.join(self.pddl_stub_out_dir, f'objects_stub_ex{e}_test{t}.pddl'))


# functions below are not used in class ObjectDetection

def search_class_hierarchy_recursively(domain_obj, object_dataframe, object_class, object_label):
    children = domain_obj.class_hierarchy.get(object_class, None)
    if children is None: return False  # reached end
    for child_class in children:
        if object_label in list(object_dataframe[child_class]['labels']): return True  # found
        search_class_hierarchy_recursively(domain_obj, object_dataframe, child_class, object_label)
    return False  # not found

def objdet_res_to_pd(objdet_res):
    return pd.DataFrame({'labels': objdet_res['labels'], 'boxes': objdet_res['boxes'].unbind()})

def object_detections_type_handling(domain_obj, objdet_res):
    objdet_by_type = domain_obj.get_detected_objects_by_types(objdet_res_to_pd(objdet_res))
    # save every object in the lowest class fin the hierarchy
    added_objects = []
    objects_type_unique_map = {}
    objects_boxes_unique_map = {}

    for k, v in objdet_by_type.items():
        for _v in list(v['labels']):
            if _v in added_objects: continue

            if search_class_hierarchy_recursively(domain_obj, objdet_by_type, k, _v) is False:  # no other subclass contains _v
                added_objects.append(_v)
                target_obj_name = _v.replace(' ', '_')  # no whitespaces for pddl syntax compatibility
                objects_type_unique_map[target_obj_name] = (k)
                objects_boxes_unique_map[target_obj_name] = \
                objdet_by_type[k][objdet_by_type[k].labels == _v].boxes.values[
                    0]  # what a syntax. you should really get rid of pd dataframes

    # assert set(added_objects)==all_uniques
    assert len(added_objects) == len(objdet_res['labels']), (len(added_objects), len(objdet_res['labels']))
    return objects_type_unique_map


def do_label_replacement(obj_type_map, replacement_dict):
    replaced_obj_type_map = {}
    for obj, typ in obj_type_map.items():
        new_label = replacement_dict[obj] if obj in replacement_dict else obj
        replaced_obj_type_map[new_label] = typ

    return replaced_obj_type_map

def do_label_replacement_dataframe_dict(obj_det_res_regular_by_type, replacement_dict):
    replaced_obj_by_type = {}
    for typ, objdf in obj_det_res_regular_by_type.items():
        det_res = objdf.to_dict(orient='list')
        for i, lab in enumerate(det_res['labels']):
            if lab in replacement_dict:
                det_res['labels'][i] = replacement_dict[lab]
        replaced_obj_by_type[typ] = pd.DataFrame(det_res)
    return replaced_obj_by_type

def argmax_iou(query_box, key_boxes):
    return box_iou(query_box.unsqueeze(0), key_boxes).argmax(dim=1)

def match_object_detections(regular, additional):
    # 1. take the max score detection for each phrase in additional (it is a REC, so referring to exactly 1 object)
    # 2. match it to the box from regular detections that has the best iou
    # 3. rename the label from the regular detection to the label from the additional detection
    max_score_box = {lab: {'score': 0, 'box': []} for lab in set(additional['labels'])}
    for box, lab, score in zip(additional['boxes'], additional['labels'], additional['logits']):
        if score > max_score_box[lab]['score']:
            max_score_box[lab]['score'] = score
            max_score_box[lab]['box'] = box  # 1

    replacement_dict = {}
    for add_obj_lab in max_score_box.keys():
        to_replace_idx = argmax_iou(max_score_box[add_obj_lab]['box'], regular['boxes'])  # 2
        replacement_dict[regular['labels'][to_replace_idx]] = add_obj_lab  # 3

    return replacement_dict  # e.g.{'vegetable':'cucumber'}

