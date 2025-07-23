import os
import hydra
from tqdm import tqdm
from hydra.utils import instantiate

from dcsgg.utils.eval_utils import (evaluate_prediction, make_example_test_pairs,
                                    predicted_triplets_from_pddl_init_state, SampleAverageMeter)
from dcsgg.utils.io_utils import require_exist

def dir_check(cfg):
    require_exist("init stubs", cfg.ss_mapping.out_dir)

def precision_recall(objdet_pred_dir, init_stub_pred_dir, dataset_obj, verbosity=0):
    domain_obj = dataset_obj.domain_obj

    # calculate precision,recall
    sample_avg_meter = SampleAverageMeter(verbosity)
    ex_test_pairs = make_example_test_pairs(dataset_obj)
    for ex_id, test_id in tqdm(ex_test_pairs):
        predicted_triplets = {"unused-name..:": predicted_triplets_from_pddl_init_state(
            os.path.join(init_stub_pred_dir, f'initstate_ex{ex_id}_test{test_id}.pddl'),
            domain_obj.lifted_predicate_args, with_truth_value=True)}

        predicted_boxes_pth = os.path.join(objdet_pred_dir, f'objdet_ex{ex_id}_test{test_id}.json')

        metrics_dict = evaluate_prediction(predicted_boxes_pth, predicted_triplets, test_id, dataset_obj, verbosity)
        sample_avg_meter.update(metrics_dict)
    return sample_avg_meter


@hydra.main(version_base=None, config_path="../conf", config_name="config")
def main(cfg):
    dir_check(cfg)
    avg_scores = instantiate(cfg.eval.prec_rec)
    avg_scores.summary()

if __name__ == "__main__":
    main()