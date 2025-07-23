# Note: The code in this file is to handle derived and unobserved predicates.
# While it explicitly defines stuff specific to the Cooking/Blocksworld/Hanoi domain,
# this should technically not be necessary. Instead, it should be readable in a domain-agnostic way from the PDDL file.
# This might be possible with the unified-planning library, but we wrote the below file as a temporary solution.
import re
import os
from hydra.utils import instantiate

from dcsgg.utils import pddl_utils

domain_obj = None
domain_name = ""
object_types = {} # key: object, value: type

# Step 3: Derived predicate functions
def cooking_is_whole(facts):
    """ (is-whole ?veg) is true if (is-sliced ?veg) is NOT present. """
    inferred = set()
    for obj, types in object_types.items():
        if "veggie" in types and ("is-sliced", obj) not in facts:
            inferred.add(("is-whole", obj))
    return inferred


def cooking_available(facts):
    """ (available ?obj) is true if no (carry ?gripper ?obj) exists. """
    carried_objects = {fact[2] for fact in facts if fact[0] == "carry"}
    inferred = {("available", obj) for obj, types in object_types.items() if
                obj not in carried_objects and 'object' in types}
    return inferred


def cooking_free(facts):
    """ (free ?gripper) is true if no (carry ?gripper ?obj) exists. """
    grippers_with_objects = {fact[1] for fact in facts if fact[0] == "carry"}
    inferred = {("free", gripper) for gripper, types in object_types.items() if
                "gripper" in types and gripper not in grippers_with_objects}
    return inferred


# def cooking_in_container(facts):
#     """ (in ?obj ?con) is true if (at ?obj ?con) exists. """
#     inferred = set()
#     for obj, types in object_types.items():
#         if "container" in types and any([(("at", fact[1], obj) in facts) for fact in facts]):
#             inferred.add(("is-whole", obj))
#     return inferred


# Step 4: Fixpoint computation to infer new facts
def cooking_infer_facts(initial_facts):
    facts = set(initial_facts)

    while True:
        derived_facts = (
                cooking_is_whole(facts) |
                cooking_available(facts) |
                cooking_free(facts) #|
                #cooking_in_container(facts)
        )

        if derived_facts.issubset(facts):
            break  # Stop if no new facts are added

        facts.update(derived_facts)

    return facts


def hanoi_clear(facts):
    """ (clear ?disk) is true if no (on ?d_other ?disk) exists """
    disks_with_disks_on_top = {fact[2] for fact in facts if fact[0] == "on"}
    inferred = {("clear", disk) for disk, types in object_types.items() if
                "disk" in types and disk not in disks_with_disks_on_top}
    return inferred


def hanoi_infer_facts(initial_facts):
    facts = set(initial_facts)

    while True:
        derived_facts = (
            hanoi_clear(facts)
        )

        if derived_facts.issubset(facts):
            break  # Stop if no new facts are added

        facts.update(derived_facts)

    return facts


def blocksworld_ontable(facts):
    """ (ontable ?block) is true if no (on ?block ?other) exists """
    blocks_with_blocks_below = {fact[1] for fact in facts if fact[0] == "on"}
    inferred = {("ontable", block) for block, types in object_types.items() if
                "block" in types and block not in blocks_with_blocks_below}
    return inferred


def blocksworld_clear(facts):
    """ (clear ?block) is true if no (on ?b_other ?block) exists """
    blocks_with_blocks_on_top = {fact[2] for fact in facts if fact[0] == "on"}
    inferred = {("clear", block) for block, types in object_types.items() if
                "block" in types and block not in blocks_with_blocks_on_top}
    return inferred


def blocksworld_handempty(facts):
    return {("handempty", robot) for robot, types in object_types.items() if "robot" in types}


def blocksworld_handfull(facts):
    return set()


def blocksworld_holding(facts):
    return set()


def blocksworld_infer_facts(initial_facts):
    facts = set(initial_facts)

    while True:
        derived_facts = (
                blocksworld_ontable(facts) |
                blocksworld_clear(facts) |
                blocksworld_handempty(facts) |
                blocksworld_handfull(facts) |
                blocksworld_holding(facts)
        )

        if derived_facts.issubset(facts):
            break  # Stop if no new facts are added

        facts.update(derived_facts)

    return facts


def expand_types(obj_type):
    expanded = set([obj_type])
    for supertype, subtypes in domain_obj.class_hierarchy.items():
        if obj_type in subtypes:
            expanded.add(supertype)
            expanded.update(expand_types(supertype))  # Recursively add parent classes
    return expanded


# This function sets the global variable object_types
def set_objects_by_type(object_definitions):
    global object_types
    object_types = {}
    # Step 1: Parse objects and their types
    for definition in object_definitions:
        obj, obj_type = definition.split(' - ')
        object_types[obj] = [obj_type]  # Store primary type as a list

    # Step 2: Expand types using class hierarchy
    # Apply expansion to all objects
    for obj, types in object_types.items():
        expanded_types = set()
        for t in types:
            expanded_types.update(expand_types(t))
        object_types[obj] = expanded_types  # Store the full hierarchy


def add_unobserved_objects(object_stub):
    if domain_name == 'blocksworld':
        prob = pddl_utils.PDDLProblem(pddl_utils.complete_stub_to_pddl_prob(object_stub))
        observed_objects = {tuple(c.replace('(', '').replace(')', '').split(' ')) for c in prob.objects}
        observed_objects |= {('arm', '-', 'robot'), }
        t = '(:objects\n'
        for objtyped in observed_objects:
            t += ' ' * 4
            for word in objtyped:
                t += word + ' '
            t += '\n'
        t += ')\n'
        return t
    return object_stub


def evaluate_init_state_with_derived_predicates(pddl_problem_with_observed_predicates):
    prob = pddl_utils.PDDLProblem(pddl_problem_with_observed_predicates)

    initial_facts = {tuple(c.replace('(', '').replace(')', '').split(' ')) for c in prob.initial_conditions}
    # print(initial_facts)

    if len(prob.objects) == 0: print('warning: emtpy object stub')
    set_objects_by_type(prob.objects)

    # Run inference
    if domain_name == 'cooking':
        final_facts = cooking_infer_facts(initial_facts)
    elif domain_name == 'hanoi':
        final_facts = hanoi_infer_facts(initial_facts)
    elif domain_name == 'blocksworld':
        final_facts = blocksworld_infer_facts(initial_facts)
    else:
        print('unknown domain', domain_name)

    # Pretty print results
    # print("\nInferred Facts:")
    # for fact in sorted(final_facts):
    #     print(fact)

    t = '(:init\n'
    for fact in sorted(final_facts):
        t += ' ' * 4 + '( '
        for word in fact:
            t += word + ' '
        t += ')\n'
    t += ')\n'
    return t



# Put (:objects (:init (:goal together
def assemble_pddl(obj, init, goal, domain_name, i):
    t = f"(define (problem {domain_name}{i})\n"
    t += f"(:domain {domain_name})\n"
    t += obj
    t += '\n'
    t += init
    t += '\n'
    t += goal
    t += '\n)\n'
    return t

def assemble_all(cfg):
    global domain_obj
    domain_obj = instantiate(cfg.domain)
    global domain_name
    domain_name = domain_obj.name
    object_stub_dir = cfg.object_detection.out_dir
    goal_stub_dir = cfg.goal_parsing.out_dir
    init_stub_dir = cfg.ss_mapping.out_dir

    problem_out_dir = cfg.planning.problempddl_out_dir
    os.makedirs(problem_out_dir, exist_ok=True)

    for e in range(1, 11):
        for i in range(1, 11):
            if e == i: continue
            if cfg.planning.verbosity > 1: print("Assembling", (e,i))
            objf = os.path.join(object_stub_dir, f'objects_stub_ex{e}_test{i}.pddl')
            initf = os.path.join(init_stub_dir, f'initstate_ex{e}_test{i}.pddl')
            goalf = os.path.join(goal_stub_dir, f'goal_stub_ex{e}_test{i}.pddl')

            with open(objf, 'r') as f:
                obj = f.read()
                obj = pddl_utils.extract_section(obj, '(:objects')
            with open(initf, 'r') as f:
                init = f.read()
                init = pddl_utils.extract_section(init, '(:init')
            with open(goalf, 'r') as f:
                goal = f.read()
                goal = pddl_utils.extract_section(goal, '(:goal')

            obj = add_unobserved_objects(obj)
            # first assemble, then evaluate_init_state_with_derived_predicates - because you need the (:object section
            # 1.
            t = assemble_pddl(obj, init, goal, domain_name, i)
            # 2.
            init_stub_with_derived = evaluate_init_state_with_derived_predicates(t)
            # print(init_stub_with_derived)
            # overwrite
            t = assemble_pddl(obj, init_stub_with_derived, goal, domain_name, i)
            with open(os.path.join(problem_out_dir, f'problem{i}_ex{e}.pddl'), 'w') as f:
                f.write(t)