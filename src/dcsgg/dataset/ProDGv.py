import os
from PIL import Image
import json

class ProDGvDataset:
    def __init__(self, domain, base_path='data'):
        self.domain_obj = domain
        self.domain_name = domain.name
        self.basepath = base_path
        if self.domain_name == 'cooking':
            self.text_query = 'chopping knife.vegetable.robotic gripper.bowl.wooden board.black tray'  # for dino-x
            # self.text_query = "kitchen knife. vegetable. robotic gripper. bowl. wooden cutting board. metal countertop."
            # self.text_query = "a kitchen knife. a tomato. a cucumber. a black robotic gripper. a white bowl. a brown round cutting board. a black countertop."
        elif self.domain_name == 'hanoi':
            self.text_query = "colored disk.wooden stick"  # dino-x
            # self.text_query = "a blue disk. a green disk. an orange disk. a yellow disk. a pink disk. a purple disk. a wooden stick."
        elif self.domain_name == 'blocksworld':
            self.text_query = "colored block"
        else:
            print("no valid domain, please specify cooking/hanoi/blocksworld.")
        self.objects = self.text_query.split('.')

    def get_imagepath(self, problem_id):
        return os.path.join(self.basepath, self.domain_name, f"observations/problem{problem_id}.jpg")

    def get_observation(self, problem_id):
        return Image.open(self.get_imagepath(problem_id))

    def get_image(self, problem_id):  # alias for get_observation
        return self.get_observation(problem_id)

    def get_domain_path(self):
        return os.path.join(self.basepath, self.domain_name, f"domain.pddl")

    def get_problem_path(self, problemid):
        return os.path.join(self.basepath, self.domain_name, "problems", f"problem{problemid}.pddl")

    def get_nl_instruction(self, problemid):
        with open(os.path.join(self.basepath, self.domain_name, "instructions", f"problem{problemid}.txt")) as f:
            return f.read()

    def get_gt_bboxes_path(self, problemid):
        return os.path.join(self.basepath, self.domain_name, "annotated_bboxes", f"problem{problemid}.json")

    def get_gt_bboxes(self, problemid):
        with open(self.get_gt_bboxes_path(problemid)) as f:
            return json.load(f)