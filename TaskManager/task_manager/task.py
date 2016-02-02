class Task:
    def __init__(self,json_dict):
        self.__dict__ = json_dict
        self.std_id = int(self.std_id)
        self.ext_id = int(self.ext_id)

    def __eq__(self,other):
        return (self.std_id == other.std_id and self.ext_id == other.ext_id)

    def __ne__(self,other):
        return not self == other

    def __str__(self):
        return "Task of type " + self.task_type + " with std_id = " + self.std_id + ", ext_id = " + self.ext_id + " and class_name = " + self.class_name


