class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return name

class Rule:
    def __init__(self, condition_list, action_list):
        self.condition_list = condition_list
        self.action_list = action_list

    def __str__(self):
        return "(" + str(condition_list) + ")"