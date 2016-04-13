import json,task

TASKS_DIR = "tasks"

def init_can_tasks(fifo_callback):
    existing_can_tasks = []
    with open('./python/TaskManager/task_manager/can_tasks.json') as json_file:
        data = json.load(json_file)
        for uselesskey,json_dict in data.iteritems():
            existing_can_tasks.append(task.Task(json_dict))
            existing_can_tasks[-1].instance = dynamic_import(TASKS_DIR,existing_can_tasks[-1].class_name)(fifo_callback)
    return existing_can_tasks

def init_user_tasks(fifo_callback):
    existing_user_tasks = []
    with open('./python/TaskManager/task_manager/user_tasks.json') as json_file:
        data = json.load(json_file)
        for uselesskey,json_dict in data.iteritems():
            existing_user_tasks.append(task.Task(json_dict))
            existing_user_tasks[-1].instance = dynamic_import(TASKS_DIR,existing_user_tasks[-1].class_name)(fifo_callback)
    return existing_user_tasks

def dynamic_import(module,class_):
    mod = __import__(module+"."+class_)
    return getattr(getattr(mod, class_),class_)

