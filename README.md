# Domain-Conditioned Scene Graphs for State-Grounded Task Planning

Code for [Domain-Conditioned Scene Graphs for State-Grounded Task Planning](https://arxiv.org/abs/2504.06661) (IROS 2025)

## Installation
```bash
conda create -n dcsgg python=3.13
conda activate dcsgg
pip install -e .

cd src/dcsgg
```

## Usage

* ➡️ Case 1: For evaluation there is `scripts/state_eval.py` and `scripts/planning_eval.py`.
* ➡️ Case 2: For execution there is `part1...py` `part2...py` `part3...py`.
* For basic usage, the two main arguments to pass are `domain` and `result_folder`.
* Advanced configuration can be edited in `conf/config.yaml`.

### ➡️ Case 1: Only measure result metrics
Presumes result files exist in a subdirectory of `results/`, e.g. `results/reported_results`.

Evaluate **State Grounding**:
```bash
python scripts/state_eval.py +domain=blocksworld result_folder=reported_results
>>> Precision | Recall: (0.98 | 1.00)
```
Evaluate **Task Planning**:
```bash
python scripts/planning_eval.py +domain=blocksworld result_folder=reported_results
>>> r_problem = 1.00  # The ratio of valid problems
>>> r_plan = 0.97     # The ratio of valid plans
>>> r_success = 0.86  # The ratio of plans that reach the goal when executed on the ground truth init state
```
### ➡️ Case 2: Run state grounding and task planning
1. Choose a name for the new subdirectory of `results/` where your results will go, e.g. `my_results`.
2. Set your API key for the LLM call during goal parsing: `export API_KEY=sk...`.

Run **State Grounding**:
```bash
# goal parsing and object detection
python part1_goal_parsing_object_detection.py +domain=cooking result_folder=my_results
# initial state generation
python part2_spatial_semantic_mapping.py +domain=cooking result_folder=my_results
```
You can measure results with `python scripts/state_eval.py +domain=cooking result_folder=my_results`.

Run **Task Planning**:
```bash
python part3_planning.py +domain=cooking result_folder=my_results
``` 
You can measure results with `python scripts/planning_eval.py +domain=cooking result_folder=my_results`.

## Understanding Result Files Layout

```commandline
results
└── reported_results 
    ├── blocksworld   
    │   ├── dinox-det       # The object detections with class prompts, pre-extracted using DINO-X API
    │   ├── objdet          # The referring expression (REC) object detections, from Grounding DINO   
    │   ├── object_stubs    # A stub of a PDDL problem containing only (:objects
    │   ├── init_stubs      # A stub of a PDDL problem containing only (:init
    │   ├── goal_stubs      # A stub of a PDDL problem containing only (:goal
    │   ├── pddl_problems   # The assembled problem.pddl
    │   └── plans           # A sequence of actions
    ├── cooking
    │   ├── dinox-det
    │   ├── ...
```
|        | [part1](src/dcsgg/part1_goal_parsing_object_detection.py)                           | [part2](src/dcsgg/part2_spatial_semantic_mapping.py)        | [part3](src/dcsgg/part3_planning.py)                               |
|--------|-------------------------------------------------------------------------------------|---------------------------------|--------------------------------------------------------|
| Input  | [Images](data/)<br/>[PDDL Domain](data/)<br/>[dinox-det](results/reported_results/) | [object_stubs]()<br/>[objdet]() | [object_stubs](results/reported_results/)<br/>[init_stubs](results/reported_results/)<br/>[goal_stubs](results/reported_results/) |
| Output | [goal_stubs](results/reported_results/)<br/>[object_stubs](results/reported_results/)<br/>[objdet](results/reported_results/)                                  | [init_stubs](results/reported_results/)                  | [PDDL Problem](results/reported_results/)<br/> [PDDL Plan](results/reported_results/)                    |

## Credits and Citation

1. [FastDownward](https://github.com/aibasel/downward/blob/main/README.md) is used within the [Unified Planning Library](https://github.com/aiplan4eu/unified-planning).
Printing credits is turned off by default.
Consider viewing them instead by setting `print_credits: True` in `config.yaml`.
2. `bin/` contains the `Validate` binary from [KCL-Planning/VAL](https://github.com/KCL-Planning/VAL). Consider installing from there instead.
3. If this repo finds use in your research, please cite:

```BibTeX
@article{herzog2025domainconditioned,
      title={Domain-Conditioned Scene Graphs for State-Grounded Task Planning}, 
      author={Jonas Herzog and Jiangpin Liu and Yue Wang},
      journal={arXiv preprint arXiv:2504.06661},
      year={2025}
}
```
