import json
import torchvision
import torch
from dcsgg.utils import pddl_utils

class SampleAverageMeter:
    def __init__(self, verbosity=0):
        self.TP = self.FN = self.FP = self.TN = 0
        self.all_correct = self.has_error = 0
        self.verbosity = verbosity

    def update(self, metrics):
        tp, fn, fp, tn = metrics['TP'], metrics['FN'], metrics['FP'], metrics['TN']
        self.TP += tp
        self.FN += fn
        self.FP += fp
        self.TN += tn
        if fn + fp == 0:
            self.all_correct += 1
        else:
            self.has_error += 1
        if self.verbosity > 1: print(f'{tp=},{fn=},{fp=},{tn=}, all correct {fn + fp == 0}')

    def summary(self):
        p = precision(self.TP, self.FP)
        r = recall(self.TP, self.FN)
        print(f'precision,recall {p, r}')
        if self.verbosity > 1: print('tp,fn,fp,tn', self.TP, self.FN, self.FP, self.TN)
        if self.verbosity > 1: print(f'problems with correct/wrong init state: {self.all_correct, self.has_error}')


class DomainAverageMeter:
    def __init__(self, verbosity=0):
        self.plan_success = self.plan_failure = 0
        self.TP = self.FN = self.FP = self.TN = 0
        self.verbosity = verbosity

    def update(self, metrics):
        self.plan_success += metrics.all_correct
        self.plan_failure += metrics.has_error
        self.TP += metrics.TP
        self.FN += metrics.FN
        self.FP += metrics.FP
        self.TN += metrics.TN

    def summary(self):
        p = precision(self.TP, self.FP)
        r = recall(self.TP, self.FN)
        print(f'overall precision,recall {p, r}')
        if self.verbosity > 1: print('tp,fn,fp,tn', self.TP, self.FN, self.FP, self.TN)
        s, f = self.plan_success, self.plan_failure
        print(f'domain planning success rate: {s}/{f}({s / (s + f)})')


def argmax_iou(query_box, key_boxes):
    return torchvision.ops.box_iou(torch.tensor([query_box]), torch.tensor(key_boxes)).argmax(dim=1)

def invert_dict(d):
    res = {}
    for key, values in d.items():
        for value in [values]:
            # For each value in the list, invert the key-value pair
            if value not in res:
                res[value] = []
            res[value].append(key)
    return res


def open_json(path):
    with open(path) as f:
        return json.load(f)


def match_object_names_by_iou(predicted_boxes_pth, gt_boxes):
    # gt_boxes: a dict with key objname, val boxes
    # each object in DET gets matched to one in GT
    name_to_gtname_dict = {}  # key: detected, value: gt
    detected_boxes = open_json(predicted_boxes_pth)  # a dict with key objname, val boxes
    for detected_obj_name, detected_obj_box in detected_boxes.items():
        # get the gt box that has the highest iou with the predicted box
        gt_max_box_id = argmax_iou(detected_obj_box, list(gt_boxes.values()))
        corresponding_gt_obj_name = list(gt_boxes)[gt_max_box_id]  # the n-th gt box
        name_to_gtname_dict[detected_obj_name] = corresponding_gt_obj_name
    # Now you mapped N-to-N objects, but it is possible that there is a detected object(in N) that is not in gt(M) so that N>M
    # so with the above lines you get double matches to gt
    # instead, match bijective, leaving possible N that do not match M open
    gtname_to_name_dict = invert_dict(name_to_gtname_dict)  # get the reverse matches from gt name to pred
    # and allow only one value per key
    for gtname, prnames in gtname_to_name_dict.items():
        n_matches = len(prnames)
        # select max iou box to keep, delete others
        pr_max_box_idx = argmax_iou(gt_boxes[gtname], [detected_boxes[n] for n in prnames])
        for idx, n in enumerate(prnames):
            if idx != pr_max_box_idx:
                print('deleted', n, 'which is not in ground truth')
                del name_to_gtname_dict[n]

    return name_to_gtname_dict



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# only provide these 1-shot examples which contain the predicate at least once
# make pairs (ex,test)
# record existing predicates
def make_example_test_pairs(dataset):
    predicates = []
    for i in range(1, 11):
        gt_init_state_list = [(t.replace('(', '').replace(')', '').split(' ')) for t in
                              pddl_utils.PDDLProblem(dataset.get_problem_path(i)).initial_conditions]
        predicates.append(set([x[0] for x in gt_init_state_list]))

    pairs = []
    for i in range(1, 11):
        problemids_with_same_predicates = [idx + 1 for idx, p in enumerate(predicates) if predicates[i - 1] == p]
        # make pairs, but don't include same sample
        pairs.extend((ex, i) for ex in problemids_with_same_predicates if ex != i)
    # print('made', len(pairs), 'pairs')
    return pairs


def predicted_triplets_from_pddl_init_state(init_state_pth, lifted_predicate_args, with_truth_value=False,
                                            observed_predicates_only=True):
    with open(init_state_pth) as f:
        pddl_prob = pddl_utils.complete_stub_to_pddl_prob(f.read())
    triplet_list = pddl_utils.PDDLProblem(pddl_prob).initial_conditions
    triplet_list = [(t.replace('(', '').replace(')', '').split(' ')) for t in triplet_list]

    if observed_predicates_only:
        # filter predicates in ground truth problem pddl that are derived not observed
        observed_predicates = lifted_predicate_args.keys()
        triplet_list = [t for t in triplet_list if t[0] in observed_predicates]

    if with_truth_value:
        triplet_list = [(t, 1) for t in triplet_list]

    return triplet_list


def get_lifted_predicate_args(dataset):
    return dataset.domain_obj.lifted_predicate_args


precision = lambda TP, FP: round(TP / (TP + FP + 1e-9), 2)
recall = lambda TP, FN: round(TP / (TP + FN + 1e-9), 2)

def evaluate_prediction(predicted_boxes_pth, predicted_triplets, problem_id, dataset, verbosity=0):
    """
    Calculates Precision and Recall of initial state predictions.

    Args:
        predicted_boxes_pth (str): The path to the json file that contains the predicted bounding boxes.
        predicted_triplets (dict): The dictionary containing the list of predicted triplets for every predicate
        problem_id (int): The test problem id within the dataset
        dataset (ProDGv): A dataset instance

    Returns:
        bool: A dictionary with {'TP','FN','FP','TN','p(recision)','r(ecall)'}

    """

    # load ground truth

    # 1. match objects from detected to GT
    gt_boxes_pth = dataset.get_gt_bboxes(problem_id)
    name_to_gtname_dict = match_object_names_by_iou(predicted_boxes_pth, gt_boxes_pth)
    if verbosity > 3: print(name_to_gtname_dict)

    # 2. load init state
    gt_triplets = predicted_triplets_from_pddl_init_state(dataset.get_problem_path(problem_id),
                                                          get_lifted_predicate_args(dataset))  # a set of (pred,obj,obj) triplets
    # gt_triplets = [list(t.predicate) for t in gt_triplets]
    if verbosity > 2: print('gt_triplets:', gt_triplets)

    pred_true_triplets = []
    pred_true_triplets_tr = []
    for _, prediction in predicted_triplets.items():  # the key in the dict is the lifted_predicate, but it is not used, so you write _ instead
        for triplet, val in prediction:
            translated_triplet = [triplet[0]] + [name_to_gtname_dict.get(e, None) for e in
                                                 triplet[1:]]  # 1st element is predicate name, then object names
            if val > 0:  # predicted true
                pred_true_triplets.append(triplet)
                pred_true_triplets_tr.append(translated_triplet)

    if verbosity > 2: print('pred_true_triplets', pred_true_triplets)
    # 3. count TP, FP, FN, TN
    TP = FN = FP = TN = 0
    for _pr, _prt in zip(pred_true_triplets, pred_true_triplets_tr):
        if _prt in gt_triplets:
            TP += 1
        else:
            FP += 1
            if verbosity > 1: print(bcolors.WARNING + 'False Positive', _pr, f'(in gt naming {_prt})' + bcolors.ENDC)

    for _gt in gt_triplets:
        if _gt not in pred_true_triplets_tr:
            FN += 1
            if verbosity > 1: print(bcolors.WARNING + 'False Negative', f'(in gt naming {_gt})' + bcolors.ENDC)

    p, r = precision(TP, FP), recall(TP, FN)
    return {k: v for k, v in locals().items() if k in {'TP', 'FN', 'FP', 'TN', 'p', 'r'}}