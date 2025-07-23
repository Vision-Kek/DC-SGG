import numpy as np
import json
import os
from tqdm import tqdm
import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

from dcsgg.utils.io_utils import make_exist_ok, require_exist
from dcsgg.utils.eval_utils import evaluate_prediction,DomainAverageMeter,SampleAverageMeter
from dcsgg.core.ss_mapping import SSMapper
from dcsgg.dataset import pddl_loader


def dir_check(cfg):
    require_exist("object_detection.out_dir", cfg.object_detection.out_dir)
    require_exist("object_detection.rec_detection_dir", cfg.object_detection.rec_detection_dir)
    require_exist("goal_parsing.out_dir", cfg.goal_parsing.out_dir)
    make_exist_ok("ss_mapping.out_dir", cfg.ss_mapping.out_dir)

def run(test_id, train_id, model, dataloader):
    train_sample = dataloader.load_gt_sample(train_id)
    model.train(*model.prepare_train_features(train_sample))

    test_sample = dataloader.load_objdet_sample(test_id, example_problem_id=train_id)
    pred = model.test(*model.prepare_test_features(test_sample))

    return pred

@hydra.main(version_base=None, config_path="conf", config_name="config")
def loop(cfg):
    dir_check(cfg)
    domain_obj = instantiate(cfg.domain)
    prodgv = instantiate(cfg.dataset)
    dataloader = pddl_loader.DataLoader(prodgv, object_stub_dir=cfg.object_detection.out_dir,
                                        objdet_dir=cfg.object_detection.rec_detection_dir)

    for example_id in tqdm(range(1,11)):
        for test_id in range(1,11):
            ss_mapper = instantiate(cfg.ss_mapping, lifted_predicate_args=domain_obj.lifted_predicate_args)
            if example_id==test_id: continue # don't include known sample
            pred = run(test_id, example_id, model=ss_mapper, dataloader=dataloader)
            ss_mapper.write_prediction(pred, test_problem_id=test_id, example_problem_id=example_id)


if __name__ == "__main__":
    loop()