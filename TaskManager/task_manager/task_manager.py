import os,sys,logging,json,task,threading,argparse,tools

debugLevel = logging.DEBUG

logging.basicConfig(level=debugLevel,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if len(sys.argv) < 3:
    logger.error("Missing args in task_manager.py ! arg1: can_fifo_rcv path, arg2: can_fifo_snd arg3: user_fifo path")
    exit()

send_fifo = None    # declared but noinitialized to avoid deadlocks
                    # as opening a fifo is blocking until another proc try to open it to
                    #thus our order to open the double fifo is can_rcv then can_snd

def send_can_message(extid,data):
    tosend = str(extid)
    for byte in data:
        tosend += ";" + str(byte)
    send_fifo.write(tosend + "\n")

existing_can_tasks = tools.init_can_tasks(send_can_message)
existing_user_tasks = tools.init_user_tasks(send_can_message)

def user_tasks_polling():
    with open(sys.argv[3],'r',0) as fifo_received:
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
            for existing_task in existing_user_tasks:
                if existing_task == new_task:
                    logger.debug("Matched a task.")
                    if existing_task.task_type == 'SOFTWARE':
    #                    existing_task.instance.set
                       # threading.Thread(target=existing_task.instance.execute(split[2::]))
                        threading.Thread(target=existing_task.instance.execute,args=(split[2::],))
                        break;
                     #elif existing_task.task_type == 'HARDWARE':

    logger.error("receive-FIFO closed")

def can_tasks_polling():
    logger.debug(sys.argv[1])
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
            for existing_task in existing_can_tasks:
                if existing_task == new_task:
                    logger.debug("Matched a task.")
                    if existing_task.task_type == 'SOFTWARE':
    #                    existing_task.instance.set
                        #threading.Thread(target=existing_task.instance.execute(split[2::]))
                        threading.Thread(target=existing_task.instance.execute,args=(split[2::],)).start()
                        break;
                     #elif existing_task.task_type == 'HARDWARE':

    logger.error("receive-FIFO closed")

if __name__ =="__main__":
    logger.debug("main started")
    threading.Thread(target=can_tasks_polling).start()
    send_fifo = open(sys.argv[2],'w',0)
    #user_tasks_polling()
