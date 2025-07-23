import os
import hydra
from tqdm import tqdm
from unified_planning.io import PDDLReader, PDDLWriter
from unified_planning.shortcuts import *
from unified_planning.engines import PlanGenerationResultStatus, ValidationResultStatus

from dcsgg.scripts import assemble_pddl_problem
from dcsgg.utils.io_utils import require_exist, make_exist_ok

def dir_check(cfg):
    require_exist("object stubs", cfg.object_detection.out_dir)
    require_exist("init stubs", cfg.ss_mapping.out_dir)
    require_exist("goal stubs", cfg.goal_parsing.out_dir)
    make_exist_ok("pddl problems", cfg.planning.problempddl_out_dir)
    make_exist_ok("plans", cfg.planning.plan_out_dir)

def generate_plans(cfg):
    if not cfg.planning.print_credits: # disable printing credits
        get_environment().credits_stream = None
    reader = PDDLReader()

    domain_path = os.path.join(cfg.data_dir, 'domain.pddl')
    generated_problem_dir = cfg.planning.problempddl_out_dir
    for problem_file in tqdm(os.listdir(generated_problem_dir)):
        problem = reader.parse_problem(domain_path,
                                       os.path.join(generated_problem_dir, problem_file))

        with OneshotPlanner() as planner:
            final_report = planner.solve(problem) # the actual call to FastDownward

        with PlanValidator() as validator:
            try:
                val_report_status = validator.validate(problem, final_report.plan).status
            except Exception as e:
                val_report_status = str(e)
        valid = val_report_status == ValidationResultStatus.VALID

        if cfg.planning.verbosity > 0:
            print("Planning", problem_file)
            print(final_report.status)
            print(val_report_status)
        if valid:
            out_dir = cfg.planning.plan_out_dir
            os.makedirs(out_dir, exist_ok=True)
            out_filepth = os.path.join(out_dir, problem_file.replace('.pddl','_plan.pddl'))
            writer = PDDLWriter(problem, needs_requirements=False)
            writer.write_plan(final_report.plan, out_filepth)

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg):
    dir_check(cfg)
    # Step 1: Assemble object_stub, init_stub and goal_stub to a pddl problem file
    if cfg.planning.assemble_first: assemble_pddl_problem.assemble_all(cfg)

    # Step 2: Let a solver (e.g. FastDownward) find the plan
    generate_plans(cfg)


if __name__ == "__main__":
    main()