def qstrs_in_label(label, query_strings):
    return any([qstr in label for qstr in query_strings])

def filter_by_labels(df, query_strings):
    return df[[qstrs_in_label(lab, query_strings) for lab in df['labels']]]

class Domain:
    def __init__(self, dir_name):
        self.name = dir_name
        
    def object2type(self, label):
        return [k for k, v in self.objecttype_map.items() if label in v][0]

    def set_class_hierarchy_bottom_up(self):
        class_hierarchy_inverted = {}
        # Loop through each key-value pair in the original dictionary
        for key, values in self.class_hierarchy.items():
            for value in values:
                # For each value in the list, invert the key-value pair
                if value not in class_hierarchy_inverted:
                    class_hierarchy_inverted[value] = []
                class_hierarchy_inverted[value].append(key)
        return class_hierarchy_inverted

    def get_detected_objects_by_types(self, objdet_df):
        # 1.
        # fill objects
        detected_objects_by_type = {}
        for k, v in self.objecttype_map.items():
            detected_objects_by_type[k] = filter_by_labels(objdet_df, v)
        return detected_objects_by_type


class Cooking(Domain):
    def __init__(self, dir_name):
        super().__init__(dir_name)
        # define types (as specified by domain.pddl)
        self.types = ['object', 'location', 'workspace', 'container', 'veggie', 'tool', 'cuttool', 'gripper']
        self.lifted_predicate_args = self.set_lifted_predicate_args()
        self.class_hierarchy = {'tool': ['cuttool'], 'object': ['veggie', 'container', 'tool'],
                                'location': ['container', 'workspace']}
        self.class_hierarchy_bottom_up = self.set_class_hierarchy_bottom_up()
        self.objecttype_map = dict(  # keys: types, values: part of a phrase
            location=['board', 'tray', 'bowl'],
            workspace=['board'],
            container=['bowl'],
            gripper=['bot'],
            tool=['knife'],
            cuttool=['knife'],
            veggie=['vegetable'],  # ['tomato', 'carrot', 'cucumber'],
            object=['vegetable', 'knife', 'bowl']  # veggies and tools and container are subcategories of objects
        )

    def set_lifted_predicate_args(self):
        # predicates
        predicates_args = {
            "at": ["object", "location"],
            "is-sliced": ["veggie"],
            "carry": ["gripper", "object"]
        }
        assert all([[p_ in self.types for p_ in args_] for args_ in predicates_args.values()])
        return predicates_args


class Hanoi(Domain):
    def __init__(self, dir_name):
        super().__init__(dir_name)
        self.name = "hanoi"
        # define types (as specified by domain.pddl)
        self.types = ['disk', 'peg']
        self.lifted_predicate_args = self.set_lifted_predicate_args()
        self.class_hierarchy = {}
        self.class_hierarchy_bottom_up = self.set_class_hierarchy_bottom_up()
        self.objecttype_map = dict(  # keys: types, values: part of a phrase
            disk=['disk'],
            peg=['stick']
        )

    def set_lifted_predicate_args(self):
        predicates_args = {
            "on": ["disk", "disk"],
            "on-peg": ["disk", "peg"],
            "smaller": ["disk", "disk"],
        }
        assert all([[p_ in self.types for p_ in args_] for args_ in predicates_args.values()])
        return predicates_args


class Blocksworld(Domain):
    def __init__(self, dir_name):
        super().__init__(dir_name)
        self.name = "blocksworld"
        # define types (as specified by domain.pddl)
        self.types = ['block']
        self.lifted_predicate_args = self.set_lifted_predicate_args()
        self.class_hierarchy = {}
        self.class_hierarchy_bottom_up = self.set_class_hierarchy_bottom_up()
        self.objecttype_map = dict(  # keys: types, values: part of a phrase
            block=['block'],
        )

    def set_lifted_predicate_args(self):
        predicates_args = {
            "on": ["block", "block"]
        }
        assert all([[p_ in self.types for p_ in args_] for args_ in predicates_args.values()])
        return predicates_args