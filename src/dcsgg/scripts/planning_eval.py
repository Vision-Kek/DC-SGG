import re
import os
import subprocess
from tqdm import tqdm
import hydra
from hydra.utils import instantiate

from unified_planning.io import PDDLReader
from unified_planning.shortcuts import PlanValidator
from unified_planning.engines import ValidationResultStatus

from dcsgg.utils.eval_utils import match_object_names_by_iou, make_example_test_pairs
from dcsgg.utils.io_utils import require_exist

print_exceptions = False
reader = PDDLReader()

def dir_check(cfg):
    require_exist("pddl problems", cfg.planning.problempddl_out_dir)
    require_exist("plans", cfg.planning.plan_out_dir)

# Check syntactical correctness of PROBLEM file
def validate_problem(domain_path, problem_path, val_bin_pth):
    try:
        output = subprocess.check_output(
            f"{val_bin_pth} {domain_path} {problem_path}",
            stderr=subprocess.STDOUT,
            shell=True,
        ).decode()

    except Exception as e:
        if print_exceptions: print('Exception in validate_problem', e)
        output = 'Exception ' + str(e)
    return output

def calc_rproblem(domain_pth, generated_problem_dir, val_bin_pth):
    print("Calculating r_problem")
    num_valid_problems = 0
    problem_files = os.listdir(generated_problem_dir)
    for problem_file in problem_files:
        #test_id, ex_id = problem_file.split('problem')[1].split('.pddl')[0].split('_ex')
        #if (int(ex_id), int(test_id)) not in ex_test_pairs: continue
        problem_path = f"{generated_problem_dir}/{problem_file}"
        output = validate_problem(domain_pth, problem_path, val_bin_pth)

        if 'exception' not in output.lower() and 'error' not in output.lower():
            num_valid_problems += 1

    r_syntax = num_valid_problems / len(problem_files)
    r_problem = r_syntax
    return r_problem

#Check if there is a valid PLAN
def validate_plan(domain_path, problem_path, plan_path):
    plan_valid = False
    problem = reader.parse_problem(domain_path,problem_path)
    try:
        plan = reader.parse_plan(problem, plan_path)
        with PlanValidator() as validator:
            val_report = validator.validate(problem, plan)
        if val_report.status == ValidationResultStatus.VALID: plan_valid = True
    except Exception as e:
        if print_exceptions: print('Exception in validate_plan:', e)
    return plan_valid

def calc_rplan(plans_dir, domain_pth, generated_problem_dir):
    print("Calculating r_plan")
    num_valid_plans = num_problems = 0

    # the loop over both problem files and plan files here is because the planner might output multiple possible plans for one problem
    # so we check if each problem has at least one valid plan
    for problem in tqdm(os.listdir(generated_problem_dir)):
        problem_name = problem.split('.pddl')[0]
        has_valid_plan = False
        for plan in os.listdir(plans_dir):
            if plan.split('_plan')[0] == problem_name and plan.endswith(".pddl"):
                # problem_name, plan_cnt = f.replace('_plan','').split('.')
                problem_path = os.path.join(generated_problem_dir, problem)
                plan_path = os.path.join(plans_dir, plan)

                plan_valid = validate_plan(domain_pth, problem_path, plan_path)
                if plan_valid:
                    has_valid_plan = True
                    break
        if has_valid_plan:
            num_valid_plans += 1
        else:
            if print_exceptions: print(problem, 'has no valid plan')
        num_problems += 1

    r_plan = num_valid_plans / num_problems
    return r_plan


# To check if the plan really reaches the goal (r_success), it must work on the ground truth initial state, not on the predicted state.
# This requires translating the names of the objects back into the dataset's names, which is only possible with the bounding boxes to match the objects by iou as you do in the metrics eval script. You call this function below:
def do_name_translation(plan_pth, translate_dict, outdir): # objdet_name->gt_name
    fname=plan_pth.split('/')[-1]
    with open(plan_pth, 'r') as src, open(f'{outdir}/{fname}', 'w') as dest:
        content = src.read()
        for key, value in translate_dict.items():
            pattern = r'\b' + re.escape(key) + r'\b'  # \b ensures it's a whole word
            content = re.sub(pattern, value, content)
        dest.write(content)


def calc_rsuccess(plans_dir, domain_name, domain_pth, generated_problem_dir, dataset_obj, pred_box_dir):
    print("Calculating r_success")
    # 1. do name translation
    name_translated_dir = os.path.join(plans_dir, 'name_translated') # create subfolder in the dir where plans are
    os.makedirs(name_translated_dir, exist_ok=True)

    for plan in os.listdir(plans_dir):
        if not plan.endswith(".pddl"): continue
        plan_path = os.path.join(plans_dir, plan)

        test_id, ex_id = plan.split('problem')[1].split('_plan')[0].split('_ex')
        predicted_boxes_pth = os.path.join(pred_box_dir, f'objdet_ex{ex_id}_test{test_id}.json')
        gt_boxes_pth = dataset_obj.get_gt_bboxes(test_id)
        translate_dict = match_object_names_by_iou(predicted_boxes_pth, gt_boxes_pth)
        # additionally translate unobserved object (there's no gt bounding box for it, it's constant, always present)
        if domain_name == 'blocksworld': translate_dict['arm'] = 'bot'

        do_name_translation(plan_path, translate_dict, name_translated_dir)

    # 2. calculate r_success
    num_successes = 0
    all_problems = os.listdir(generated_problem_dir)

    ex_test_pairs = make_example_test_pairs(dataset_obj)
    for problem in tqdm(all_problems):
        problem_name = problem.split('.pddl')[0]
        has_valid_plan = False
        for plan in os.listdir(name_translated_dir):
            if plan.split('_plan')[0] == problem_name:
                plan_path = os.path.join(name_translated_dir, plan)
                test_id, ex_id = plan.split('problem')[1].split('_plan')[0].split('_ex')
                # only evaluate on the example-test pairs provided
                if (int(ex_id), int(test_id)) not in ex_test_pairs: continue

                gt_problem_path = dataset_obj.get_problem_path(test_id)
                # print('eval', plan, ', in gt:', gt_problem_path)
                plan_valid = validate_plan(domain_pth, gt_problem_path, plan_path)
                if plan_valid: has_valid_plan = True
        if has_valid_plan: num_successes += 1

    return num_successes / len(ex_test_pairs)

@hydra.main(version_base=None, config_path="../conf", config_name="config")
def main(cfg):
    dir_check(cfg)
    r_problem = instantiate(cfg.eval.r_problem)
    print(f'{r_problem=}')

    r_plan = instantiate(cfg.eval.r_plan)
    print(f'{r_plan=}')

    r_success = instantiate(cfg.eval.r_success)
    print(f'{r_success=}')

if __name__ == "__main__":
    main()