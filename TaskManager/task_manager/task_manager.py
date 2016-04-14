import sys
import logging
import task
import threading
import tools
import socket

debugLevel = logging.DEBUG

logging.basicConfig(level=debugLevel,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if len(sys.argv) < 3:
    logger.error("Missing args in task_manager.py ! \
                 arg1: can_socket path, arg2: user_fifo path")
    exit()

can_socket_fd = None  # just so it's not undefined


def send_can_message(extid, data):
    tosend = str(extid)
    for byte in data:
        tosend += ";" + str(byte)
        can_socket_fd.write(tosend + "\n")

existing_can_tasks = tools.init_can_tasks(send_can_message)
existing_user_tasks = tools.init_user_tasks(send_can_message)


def user_tasks_polling(can_socket_fd):
    logger.debug("receive-FIFO opened.")
    while(True):
        split = can_socket_fd.readline().split(";")
        if len(split) < 2:
            break
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
                    threading.Thread(target=existing_task.instance.execute,
                                     args=(split[2::],))
                    break
#                elif existing_task.task_type == 'HARDWARE':
                    logger.error("receive-FIFO closed")


def can_tasks_polling(can_socket_fd):
    logger.debug("receive-FIFO opened.")
    while(True):
        split = can_socket_fd.readline().split(";")
        if len(split) < 2:
            break
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
                    threading.Thread(target=existing_task.instance.execute,
                                     args=(split[2::],)).start()
                    break
#                elif existing_task.task_type == 'HARDWARE':

    logger.error("receive-FIFO closed")


if __name__ == "__main__":
    logger.debug("main started")
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    can_socket = sock.connect(sys.argv[1]).makefile()
    threading.Thread(target=can_tasks_polling, params=(can_socket,)).start()
#   user_tasks_polling()
