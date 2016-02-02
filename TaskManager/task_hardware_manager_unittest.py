#! /usr/bin/python
import unittest,threading,os
from task_manager.task_manager import TaskManager
from task_manager.actions import *
from subprocess import call

def startTaskManager():
	taskManager = TaskManager(FIFO_PATH)
	taskManager.start()
	
FIFO_PATH = "/tmp/fifo"

try:
	os.unlink(FIFO_PATH)
except:
	print ""
	
os.mkfifo(FIFO_PATH)

threading.Thread(target=startTaskManager).start()
call(["./fifo_writing_cpp/a.out",FIFO_PATH])
#fifo_write = open(FIFO_PATH, 'w')
#print "opened write-end"

while(True):
	line = raw_input() + "\n"
	#fifo_write.write(line)
	#fifo_write.flush()


