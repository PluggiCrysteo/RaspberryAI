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

class message_sender:
    def set_fd(self,fd):
        self.fd = fd

    def send_can_message(self,extid, data):
        tosend = str(extid)
        for byte in data:
            tosend += ";" + str(byte)
        logger.debug("writing to the can_server:")
        logger.debug(tosend)
        self.fd.write(tosend + "\n")

sender = message_sender()

existing_can_tasks = tools.init_can_tasks(sender.send_can_message)
existing_user_tasks = tools.init_user_tasks(sender.send_can_message)

# TODO shouldn't have refractored this actually
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

    logger.error("can_unix_socket closed")


if __name__ == "__main__":
    logger.debug("main started")
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(sys.argv[1])
    can_socket = sock.makefile('rw',0)
    sender.set_fd(can_socket)
    threading.Thread(target=can_tasks_polling, args=(can_socket,)).start()
#   user_tasks_polling()
