import os

from dcsgg.utils import pddl_utils

class GoalParser:
    def __init__(self, llm, dataset, out_dir, verbosity):
        self.llm = llm
        self.dataset = dataset
        self.domain_dict = self.build_domain_dict()
        self.verbosity = verbosity
        self.out_dir = out_dir

    def build_domain_dict(self):
        domain_dict = {}
        pddl_domain_txt = open(self.dataset.get_domain_path()).read()
        domain_dict['types'] = pddl_utils.extract_section(pddl_domain_txt, '(:types')
        domain_dict['predicates'] = pddl_utils.extract_section(pddl_domain_txt, '(:predicates')
        domain_dict['obj_phrases'] = [s.strip() for s in self.dataset.text_query.split('.') if len(s) > 0]
        return domain_dict

    def assemble_prompt(self, example, new):
        prompt="Your task is to generate a PDDL goal state given a natural language instruction, the PDDL types and predicates from the domain file, and some object referrals. You should reuse the existing object referrals or domain types whenever possible, only if the NL instruction includes objects which cannot be unambiguously matched with the object referrals, in this case you may include a new object in the goal state. Answer only, no explanation please.\n\n"
        prompt+="Here's the PDDL domain:\n"
        prompt+=self.domain_dict['types']
        prompt+=self.domain_dict['predicates']
        prompt+="\nAnd here are the object phrases: "
        prompt+=str(self.domain_dict['obj_phrases'])
        prompt+='\n\nEXAMPLE:\n'
        prompt+='\nQ:\n' #INPUT
        prompt+='NL instruction: '+example['instruction']
        prompt+='\nA:\n' #OUTPUT
        prompt+=example['output']
        prompt+='\n\nNow, a new instruction:\n'
        prompt+='\nQ:\n' #INPUT
        prompt+='NL instruction: '+new['instruction']
        prompt+='\nA:\n' #OUTPUT
        return prompt

    def screen_goal_for_unreferred_objects(self, goal):
        gdinophrases = self.domain_dict['obj_phrases']
        obj_refs_in_goal_but_not_in_gdinophrases = []
        for line in goal:
            condition = line.replace('(', '').replace(')', '').split(' ')
            if condition[0] == 'forall': continue  # forall lines do not contain a variable, but iterates over types
            for objref in condition[1:]:  # the first arg is the predicatename, the following the obj refs
                if objref[0] != '?':  # a local variable (starting with ?) instead of an object name
                    if objref not in gdinophrases:
                        obj_refs_in_goal_but_not_in_gdinophrases.append(objref)
        return obj_refs_in_goal_but_not_in_gdinophrases

    def run(self, example_problem_id, test_problem_id):
        example_dict = {}
        ex_pddl_domprob = pddl_utils.PDDLProblem(self.dataset.get_problem_path(example_problem_id))
        ex_pddl_problem = open(self.dataset.get_problem_path(example_problem_id)).read()
        example_dict['instruction'] = self.dataset.get_nl_instruction(example_problem_id)
        example_dict['goal_set'] = ex_pddl_domprob.goal_conditions
        example_dict['goal_str'] = pddl_utils.extract_section(ex_pddl_problem, '(:goal')

        example_dict['output'] = example_dict['goal_str']

        test_problem_dict = {'instruction': self.dataset.get_nl_instruction(test_problem_id)}  # the test sample

        prompt = self.assemble_prompt(example_dict, test_problem_dict)
        if self.verbosity > 2: print(f'{prompt=}')
        # the lmm call
        goal_llm_pred = self.llm.withpromttext(prompt)
        if self.verbosity > 1: print(goal_llm_pred)

        parsed_goal = pddl_utils.PDDLProblem(pddl_utils.complete_stub_to_pddl_prob(goal_llm_pred)).goal_conditions
        missing_obj_referral_phrases = self.screen_goal_for_unreferred_objects(parsed_goal)
        if self.verbosity > 1: print(f'{missing_obj_referral_phrases=}')
        return goal_llm_pred, missing_obj_referral_phrases

    def write_prediction(self, goal_llm_pred, example_problem_id, test_problem_id):
        e, t = example_problem_id, test_problem_id
        with open(os.path.join(self.out_dir, f'goal_stub_ex{e}_test{t}.pddl'), 'w') as f:
            f.write(goal_llm_pred)