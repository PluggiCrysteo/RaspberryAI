import os,sys,logging,json,task,threading,argparse

debugLevel = logging.DEBUG

logging.basicConfig(level=debugLevel,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if len(sys.argv) < 2:
    logger.error("Missing args in task_manager.py !")
    exit()

TASKS_DIR = "tasks"

def dynamic_import(module,class_):
    mod = __import__(module+"."+class_)
    return getattr(getattr(mod, class_),class_)

#def fifo_callback(can_message)
    

existing_tasks = []
instances = []

with open('tasks.json') as json_file:
    data = json.load(json_file)
    for uselesskey,json_dict in data.iteritems():
        existing_tasks.append(task.Task(json_dict))
        existing_tasks[-1].instance = dynamic_import(TASKS_DIR,existing_tasks[-1].class_name)()
        

with open(sys.argv[1],'r',0) as fifo_received:
    logger.debug("receive-FIFO opened.")
    while(True):
        split = fifo_received.readline().split(";")
        if len(split) < 2:
            break;
        new_task_dict = {}
        new_task_dict['std_id'] = int(split[0])
        new_task_dict['ext_id'] = int(split[1])
        new_task = task.Task(new_task_dict)
        logger.debug("Standard ID: " + split[0])
        logger.debug("Extended ID: " + split[1])
        for existing_task in existing_tasks:
            if existing_task == new_task:
                logger.debug("Matched a task.") 
                if existing_task.task_type == 'SOFTWARE':
#                    existing_task.instance.set
                    threading.Thread(target=existing_task.instance.execute(split[2::]))
                    break;
                 #elif existing_task.task_type == 'HARDWARE':

    logger.error("receive-FIFO closed")
