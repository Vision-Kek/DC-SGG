import re
import os

def extract_section(pddl, section_keyphrase, open_bracket='(', close_bracket=')'):
    if pddl.endswith('.pddl'):  # can take both string or file
        with open(pddl, 'r') as f:
            pddl = f.read()

    # Initialize counters and variables to track the content
    open_count = 0
    extracted_content = []
    start_idx = pddl.find(section_keyphrase)  # start to count from here
    start_idx = pddl.rfind('\n', 0, start_idx) + 1  # include trailing whitespaces
    # Traverse through the string
    for char in pddl[start_idx:]:
        extracted_content.append(char)

        if char == open_bracket:
            open_count += 1
        elif char == close_bracket:
            open_count -= 1
            if open_count == 0:  # Closing bracket matches the opening one
                break

    return ''.join(extracted_content) if open_count == 0 else None


def remove_section(domainfile, section_name, outfile):
    os.system(f'cp {domainfile} {outfile}')
    while True:
        dblock = extract_section(outfile, section_name)
        if dblock is None: break
        with open(outfile, 'r') as _f:
            s = _f.read()
        with open(outfile, 'w') as _f:
            _f.write(s.replace(dblock, ''))


def complete_stub_to_pddl_prob(stub, domain_name='unnamed'):
    t = "(define (problem unnamed)\n"
    t += f"(:domain {domain_name})\n"
    for sec in ('(:objects', '(:init', '(:goal'):
        if sec not in stub:
            t += f'\n{sec})\n'
        else:
            t += stub
    t += '\n)'
    return t



class PDDLProblem:
    def __init__(
            self,
            pddl_problem: str,
    ):
        if pddl_problem.endswith('.pddl'):
            pddl_problem = open(pddl_problem).read()

        self.pddl_problem = pddl_problem
        self.pddl_problem_flat = re.sub(
            r"\s+", " ",  # replace multiple whitespaces through one
            pddl_problem.replace("\n", " "),
        )

        self.parse_objects()
        self.parse_initial_state()
        self.parse_goal_specification()

    # parse (:object * ) w/o newline
    def parse_objects(self):
        try:
            self.pddl_objects = extract_section(self.pddl_problem, '(:objects')
            text = re.findall(
                r"\(:objects.*\(:init",
                self.pddl_problem_flat,
            )[0].replace("(:init", "")

            text = text.replace("(:objects", "")
            text = text.replace(")", "")
            text = text.strip().rstrip()

            type_flag = False
            buff = []
            objects = []

            for x in text.split(" "):
                if type_flag:
                    for b in buff:
                        objects += [f"{b} - {x}"]

                    buff.clear()
                    type_flag = False
                elif x == "-":
                    type_flag = True
                else:
                    buff += [x]

            # in case types are not used
            if len(buff) > 0:
                for b in buff:
                    objects += [f"{b}"]

            self.objects = objects
        except Exception as e:
            print(e)
            self.pddl_objects = []
            self.objects = []

    # parse (:init * ) w/o newline
    def parse_initial_state(self):
        try:
            self.pddl_initial_state = extract_section(self.pddl_problem, '(:init')
            text = re.findall(
                r"\(:init.*\(:goal",
                self.pddl_problem_flat,
            )[0].replace("(:goal", "")

            text = text.replace("(:init", "")
            text = text.replace("(", " ( ")
            text = text.replace(")", " ) ")
            text = re.sub(r"\s+", " ", text)
            text = text.strip().rstrip()

            buff = []
            count = 0

            conditions = []

            for x in text.split(" "):
                if x == "(":
                    count += 1
                elif x == ")":
                    if len(buff) > 0:
                        conditions += ["(" + " ".join(buff) + ")"]
                        buff.clear()

                    count -= 1
                else:
                    buff += [x]

                if count < 0:
                    break

            self.initial_conditions = conditions
        except Exception as e:
            print(e)
            self.pddl_initial_state = []
            self.initial_conditions = []

    # parse (:goal * )* w/o newline
    def parse_goal_specification(self):
        try:
            self.pddl_goal_specification = extract_section(self.pddl_problem, '(:goal')
            text = re.findall(
                r"\(:goal.*",
                self.pddl_problem_flat,
            )[0]

            text = text.replace("(:goal", "")
            text = text.replace("(and", "", 1)
            text = text.replace("(", " ( ")
            text = text.replace(")", " ) ")
            text = re.sub(r"\s+", " ", text)
            text = text.strip().rstrip()

            buff = []
            count = 0

            conditions = []

            for x in text.split(" "):
                if x == "(":
                    count += 1
                elif x == ")":
                    if len(buff) > 0:
                        conditions += ["(" + " ".join(buff) + ")"]
                        buff.clear()

                    count -= 1
                else:
                    buff += [x]

                if count < 0:
                    break

            self.goal_conditions = conditions
        except Exception as e:
            print(e)
            self.pddl_goal_specification = []
            self.goal_conditions = []