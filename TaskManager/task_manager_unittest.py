#! /usr/bin/python
import task_manager, unittest,threading,os

def startTaskManager():
	taskManager = task_manager.TaskManager(FIFO_PATH)
	taskManager.start()
	
FIFO_PATH = "/tmp/fifo"

os.unlink(FIFO_PATH)
os.mkfifo(FIFO_PATH)

threading.Thread(target=startTaskManager).start()

fifo_write = open(FIFO_PATH, 'w')
print "opened write-end"

while(True):
	line = raw_input() + "\n"
	fifo_write.write(line)
	fifo_write.flush()


