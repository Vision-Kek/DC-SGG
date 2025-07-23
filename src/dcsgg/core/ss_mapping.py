import os
import numpy as np
import math

def min_distance_between_bboxes(box1, box2):
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    dx = max(x2_min - x1_max, x1_min - x2_max, 0)  # Horizontal gap
    dy = max(y2_min - y1_max, y1_min - y2_max, 0)  # Vertical gap
    # The distance is zero if the boxes overlap
    return math.sqrt(dx**2 + dy**2)

f1 = lambda b1,b2: b2[0]-b1[0]
f2 = lambda b1,b2: b2[1]-b1[1]
f3 = lambda b1,b2: b2[2]-b1[2]
f4 = lambda b1,b2: b2[3]-b1[3]

uf1,uf2,uf3,uf4,uf5,uf6 = lambda b:b[3]-b[2], lambda b:b[3]-b[1], lambda b:b[3]-b[0], lambda b:b[2]-b[1], lambda b:b[2]-b[0], lambda b:b[1]-b[0]

function_registry = f1, f2, f3, f4, lambda a1,a2: min_distance_between_bboxes(a1,a2)*4
function_registry_unary = uf1,uf2,uf3,uf4,uf5,uf6

def make_triplets(relation_dict, objdet_by_type):
    spatialtriplets = {}
    for _rel, object_type_pair in relation_dict.items():
        predicate_key = _rel + ":" + str(object_type_pair)
        spatialtriplets[predicate_key] = []
        for ks, vs in objdet_by_type.items():  # subjects,# iteration over type
            # print('j',_rel,ks, object_type_pair)
            for ko, vo in objdet_by_type.items():  # objects, # iteration over type
                # check if this subject-object pair matches types that can form a pair in this domain
                if [ks, ko] == object_type_pair:
                    # then add the triplets (a set of spatial relations)
                    for slab, sbox, in vs.items():  # iteration over instance
                        for olab, obox in vo.items():  # iteration over instance
                            if slab != olab:  # don't consider relationship to itself
                                for frel in function_registry:
                                    spatialtriplets[predicate_key].append((slab, frel, frel(sbox, obox), olab))

            if [ks] == object_type_pair:  # only one element (ks) for single-arg-predicates
                for slab, sbox in vs.items():  # iteration over instance
                    for frel in function_registry_unary:
                        spatialtriplets[predicate_key].append((slab, frel, frel(sbox)))
    return spatialtriplets

def extract_features_of_semantic_triplet(triplets, s_trip):
    sub_idx, fn_idx, val_idx, obj_idx = 0, 1, 2, 3
    res = {'fn': [], 'val': []}
    if len(s_trip) == 2:  # unary
        equality = lambda _trip: _trip[sub_idx] == s_trip[1]
    else:  # binary
        equality = lambda _trip: _trip[sub_idx] == s_trip[1] and _trip[obj_idx] == s_trip[2]  # _rel,_sub,_obj=s_trip
    for triplet in triplets:
        if equality(triplet):
            res['fn'].append(triplet[fn_idx])
            res['val'].append(triplet[val_idx])
    return res


def semantic_triplets(relation_key, spatial_triplets):
    sub_idx, fn_idx, val_idx, obj_idx = 0, 1, 2, 3
    triplets = []
    for sp_triplet in spatial_triplets:
        subject_object_pair = [sp_triplet[0], sp_triplet[-1]] if len(sp_triplet) == 4 else [
            sp_triplet[0]]  # handle unary with no objects
        triplet = (relation_key.split(':')[0], *subject_object_pair)
        if triplet not in triplets:
            triplets.append(triplet)
    return triplets


def assemble_triplet_feats(triplets):
    triplet_feats = {}
    sem_triplets = {}  # key: relation-type, value: object-rel-object triplets
    for relation_key, triplet_list in triplets.items():
        # print(relation_key)
        sem_triplets[relation_key] = semantic_triplets(relation_key, triplet_list)
        triplet_feats[relation_key] = [extract_features_of_semantic_triplet(triplet_list, s_tripl)['val'] for s_tripl in
                                       sem_triplets[relation_key]]
    return triplet_feats, sem_triplets


def assemble_triplet_feats_from_gt(triplets, gt_state, debug=False):
    true_triplet_feats = {}
    false_triplet_feats = {}
    for relation_key, triplet_list in triplets.items():
        if debug: print('processsing rel', relation_key, f'with {len(triplet_list)} triplets')
        true_triplet_feats[relation_key] = []
        false_triplet_feats[relation_key] = []
        true_triplets = [s.strip('( )').split(' ') for s in gt_state.split('\n')[1:-1]]
        if debug: print('true triplets', true_triplets)
        for semtriplet in semantic_triplets(relation_key, triplet_list):
            if debug: print('processing trip', semtriplet)
            # pr,sub,obj=semtriplet
            # if [pr,sub,obj] in true_triplets or (sub==obj and [pr,sub] in true_triplets): # 2nd option for unary predicates
            if list(semtriplet) in true_triplets:
                if debug: print('add', relation_key, semtriplet)
                true_triplet_feats[relation_key].append(
                    extract_features_of_semantic_triplet(triplet_list, semtriplet)['val'])
            else:
                false_triplet_feats[relation_key].append(
                    extract_features_of_semantic_triplet(triplet_list, semtriplet)['val'])
    return true_triplet_feats, false_triplet_feats


def nn_store(pos_feats, neg_feats, verbosity):
    # the model is just the feature set
    model = (pos_feats, neg_feats)
    return model

def nn_predict(model, semtripl, testfeats, verbosity):
    gfp,gfn = model
    res = []
    for i in range(len(testfeats)):
        tf = np.array(testfeats[i])

        dist_to_pos = np.linalg.norm(tf-gfp, axis=1)
        dist_to_neg = np.linalg.norm(tf-gfn, axis=1)
        #print(dist_to_pos.shape, dist_to_neg.shape)
        mindistp, mindistn = dist_to_pos.min(), dist_to_neg.min()
        predval = 1 if mindistp < mindistn else 0
        if verbosity>2: print(f'classify {semtripl[i]} as {mindistp < mindistn}')
        res.append((semtripl[i],predval))
    return res


def write_predicted_init_state(pred, outfile):
    pddl_str='(:init\n'
    for pr,triplet_list in pred.items():
        for triplet,value in triplet_list:
            if value>0:
                [word+' ' for word in triplet]
                pddl_str+=f'{" "*4}({" ".join(triplet)})\n'
    pddl_str+=')\n'

    with open(outfile,'w') as f:
        f.write(pddl_str)


class SSMapper:
    def __init__(self, lifted_predicate_args, out_dir, verbosity=0):
        self.train_method = nn_store
        self.test_method = nn_predict
        self.out_dir = out_dir
        self.lifted_predicate_args = lifted_predicate_args
        self.verbosity = verbosity
        self.models = None # to be initialized in train()

    def prepare_train_features(self, train_sample):
        # make triplets of candidate pairs and functions (sub,fn,val,obj)
        triplets = make_triplets(relation_dict=self.lifted_predicate_args,
                                 objdet_by_type=train_sample['objdet_by_type'])
        assembled_feats_pos, assembled_feats_neg = assemble_triplet_feats_from_gt(triplets, train_sample["init_state"],
                                                                                  debug=self.verbosity>3)
        return assembled_feats_pos, assembled_feats_neg

    def prepare_test_features(self, test_sample):
        # make triplets of candidate pairs and functions (sub,fn,val,obj)
        triplets = make_triplets(relation_dict=self.lifted_predicate_args,
                                 objdet_by_type=test_sample['objdet_by_type'])

        in_features, _sem_triplets = assemble_triplet_feats(triplets)
        return in_features, _sem_triplets

    def train(self, assembled_feats_pos, assembled_feats_neg):
        models = {}

        assert (assembled_feats_pos.keys() == assembled_feats_neg.keys())
        # fit model for each predicate
        for predicate in assembled_feats_pos.keys():
            if len(assembled_feats_pos[predicate]) == 0:
                if self.verbosity > 1: print('Warning:', predicate, 'is never true in example, SKIPPING')
                continue
            elif len(assembled_feats_neg[predicate]) == 0:
                if self.verbosity > 1: print('Warning:', predicate, 'is always true in example,SKIPPING')
                continue

            pf, nf = assembled_feats_pos[predicate], assembled_feats_neg[predicate]
            model = self.train_method(pf, nf, self.verbosity)
            models[predicate] = model
        self.models = models

    def test(self, testfeats, semtripl):
        res = {}
        for predicate in self.models.keys():
            res[predicate] = self.test_method(
                self.models[predicate], semtripl[predicate], testfeats[predicate], self.verbosity)
        return res

    def write_prediction(self, pred, example_problem_id, test_problem_id):
        e,t = example_problem_id, test_problem_id
        write_predicted_init_state(pred, os.path.join(self.out_dir, f'initstate_ex{e}_test{t}.pddl'))