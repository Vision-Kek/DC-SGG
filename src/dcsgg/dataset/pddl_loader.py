import json
import os

import dcsgg.utils.pddl_utils as pddl_utils
from dcsgg.utils.io_utils import open_json


def parse_objects_from_pddl_stub(object_pddl_section):
    t = pddl_utils.complete_stub_to_pddl_prob(object_pddl_section)
    obj_list = pddl_utils.PDDLProblem(t).objects
    obj_by_type = {}
    for l in obj_list:
        objs, objtype = l.split(' - ')
        objs = objs.split(' ')
        for obj in objs:
            obj_by_type[obj] = objtype
    return obj_by_type


def update_nested_dict(key, target_dict, target_value):
    if key not in target_dict:
        target_dict[key] = target_value  # copy label-box-dict to superclass key
    else:
        for k, v in target_value.items():
            target_dict[key][k] = v  # existing entry, dont overwrite but add

def superclasses(k, class_hierarchy_bottom_up):
    return class_hierarchy_bottom_up.get(k, [])

def add_all_superclasses(obj_by_type_dict, class_hierarchy_bottom_up):
    obj_by_type_dict_with_superclasses = obj_by_type_dict.copy()
    for k, labelboxdict in obj_by_type_dict.items():
        for ksup in superclasses(k, class_hierarchy_bottom_up):
            update_nested_dict(ksup, obj_by_type_dict_with_superclasses, labelboxdict)
            for ksupl2 in superclasses(ksup, class_hierarchy_bottom_up):
                update_nested_dict(ksupl2, obj_by_type_dict_with_superclasses, labelboxdict)
                for ksupl3 in superclasses(ksupl2, class_hierarchy_bottom_up):
                    update_nested_dict(ksupl3, obj_by_type_dict_with_superclasses, labelboxdict)
                    # ... you just make three layers here, don't want to write some recursive thing
    return obj_by_type_dict_with_superclasses

def read_types_from_object_pddl(objdet_json, object_pddl_section, class_hierarchy_bottom_up):
    obj_type_dict = parse_objects_from_pddl_stub(object_pddl_section)  # key: object, value:type
    with open(objdet_json) as f:
        obj_det_dict = json.load(f)

    alltypes = list(obj_type_dict.values())
    obj_by_type_dict = {k: {} for k in alltypes}  # key:type, value:objects
    for lab, box in obj_det_dict.items():
        obj_by_type_dict[obj_type_dict[lab]][lab] = box

    obj_by_type_dict = add_all_superclasses(obj_by_type_dict, class_hierarchy_bottom_up)
    return obj_by_type_dict


class DataLoader:
    def __init__(self, dataset_obj, object_stub_dir, objdet_dir):
        self.dataset = dataset_obj
        self.domain_obj = dataset_obj.domain_obj
        self.object_stub_dir = object_stub_dir
        self.objdet_dir = objdet_dir

    def load_gt_sample(self, problemid):
        # 1. read objdet dataframe
        objdet = self.dataset.get_gt_bboxes_path(problemid)
        object_pddl = pddl_utils.extract_section(self.dataset.get_problem_path(problemid), '(:objects')
        # 2. match every object to the type listed in the pddl object
        objdet_by_type = read_types_from_object_pddl(objdet, object_pddl, self.domain_obj.class_hierarchy_bottom_up)
        init_state = pddl_utils.extract_section(self.dataset.get_problem_path(problemid), section_keyphrase='(:init')
        return {'objdet_by_type': objdet_by_type, 'init_state': init_state}


    def load_objdet_sample(self, problem_id, example_problem_id):
        pddlobjstub_filepath = os.path.join(self.object_stub_dir,
                                            f'objects_stub_ex{example_problem_id}_test{problem_id}.pddl')
        objdet_filepath = os.path.join(self.objdet_dir,
                                       f'objdet_ex{example_problem_id}_test{problem_id}.json')

        object_pddl = pddl_utils.extract_section(pddlobjstub_filepath, '(:objects')
        objdet_by_type = read_types_from_object_pddl(objdet_filepath, object_pddl, self.domain_obj.class_hierarchy_bottom_up)
        return {'objdet_by_type': objdet_by_type}