import os
import hydra
from tqdm import tqdm
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

from dcsgg.utils.io_utils import make_exist_ok, require_exist
from dcsgg.core import goal_parsing
from dcsgg.core import object_detection


def dir_check(cfg):
    make_exist_ok("result_dir", cfg.result_dir)
    make_exist_ok("goal_parsing.out_dir", cfg.goal_parsing.out_dir)
    make_exist_ok("object_detection.rec_detection_dir", cfg.object_detection.rec_detection_dir)
    make_exist_ok("object_detection.out_dir", cfg.object_detection.out_dir)
    dinoxdir = cfg.object_detection.dinox_detection_dir
    if not os.path.exists(dinoxdir):
        src = f'{cfg.repo_root}/results/reported_results/{cfg.domain.dir_name}/dinox-det'
        print("Copying dinox_detection_dir from reported results")
        os.system(f"cp -r {src} {dinoxdir}")
    else:
        print("Using existing dinox_detection_dir")


@hydra.main(version_base=None, config_path="conf", config_name="config")
def loop(cfg):
    dir_check(cfg)
    # setup dataset and domain
    domain_obj = instantiate(cfg.domain)
    prodgv = instantiate(cfg.dataset)

    # setup goalparser and objectdetector
    goal_parser = instantiate(cfg.goal_parsing, dataset=prodgv)
    object_detector = instantiate(cfg.object_detection, dataset=prodgv)

    test_sample_ids = list(range(1, 11))
    example_sample_ids = list(range(1, 11))

    for test_problem_id in tqdm(test_sample_ids):  # sample test problem
        for example_problem_id in example_sample_ids:  # sample example problem
            if example_problem_id == test_problem_id: continue
            if cfg.goal_parsing.verbosity + cfg.object_detection.verbosity > 0:
                print('(test, example)', test_problem_id, example_problem_id)

            # the llm call
            goal_llm_pred, missing_obj_referral_phrases = goal_parser.run(example_problem_id, test_problem_id)
            goal_parser.write_prediction(goal_llm_pred, example_problem_id, test_problem_id)

            # 1. load detections on regular phrases
            obj_det_res_regular = object_detector.load_regular_detections(test_problem_id)
            objects_type_map = object_detection.object_detections_type_handling(domain_obj, obj_det_res_regular)

            # 2. load the potential additional objects
            replacement_dict = {}
            if len(missing_obj_referral_phrases) > 0:
                # detect the objects that the LLM included but are not in regular phrases
                obj_det_res_additional = object_detector.supplemental_object_detection(
                    set(missing_obj_referral_phrases), test_problem_id)
                if len(obj_det_res_additional['labels']) > 0:  # object detection res not empty
                    replacement_dict = object_detection.match_object_detections(obj_det_res_regular, obj_det_res_additional)
                    if cfg.object_detection.verbosity > 2: print(f'{replacement_dict=}')
                    objects_type_map = object_detection.do_label_replacement(objects_type_map, replacement_dict)

            object_detector.write_pddl_object_stubs(objects_type_map=objects_type_map, test_id=test_problem_id, example_id=example_problem_id)
            object_detector.write_detections(replacement_dict, test_problem_id, example_problem_id)


if __name__ == "__main__":
    loop()