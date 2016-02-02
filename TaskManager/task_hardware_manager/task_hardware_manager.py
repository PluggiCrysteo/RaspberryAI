#! /usr/bin/python

import logging,time,threading,os,sys
from task_hardware import TaskHardware

debugLevel = logging.INFO
logger = logging.getLogger("TaskManager")

if len(sys.argv) > 1 and sys.argv[1] == "-d":
	debugLevel = logging.DEBUG

logging.basicConfig(level=debugLevel,format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class TaskManager:

	def __init__(self,fifoPath):
		self.tasks = []
		self.fifoPath = fifoPath
		self.taskUpdateLock = threading.Lock()

		
	def start(self):
	
		logger.info("starting the readNamedPipe thread")
		taskUpdaterThread = threading.Thread(target=self.read_named_pipe)
		taskUpdaterThread.start()
		currentTask = None
		
		logger.info("starting the loop (executing tasks)")
		while(True):
			time.sleep(0.5)
			if not self.tasks:		## no need to keep going if lsit is empty
				continue
				
			logger.debug("tasks was not empty")
			
			self.taskUpdateLock.acquire()			## aint modifying tasks
			
			if currentTask != None and currentTask.state == Task.FINISHED:		## popping finished task
				self.tasks.remove(currentTask)
				if not self.tasks:		## no need to keep going if lsit is empty
					continue		
				self.tasks.sort(key= lambda x : x.value, reverse = True)	## ordering tasks to get the best one
				currentTask = self.tasks[0]
				currentTask.start()
				
			elif currentTask == None:		
				self.tasks.sort(key= lambda x : x.value, reverse = True)	## ordering tasks to get the best one
				currentTask = self.tasks[0]	
			else:
				self.tasks.sort(key= lambda x : x.value, reverse = True)	## ordering tasks to get the best one
				if self.tasks[0] < currentTask:
					currentTask.pause()
					currentTask = self.tasks[0]
					currentTask.start()
				
			self.taskUpdateLock.release()		## release lock, can be interupted again

	def read_named_pipe(self):
		with open(self.fifoPath, 'r',0) as fifo_read:
			logger.debug("Opened the reading-end of the caca fifo")
			while(True):
			        line = fifo_read.readline()
				taskArr = line.split(";")
				self.taskUpdateLock.acquire()
                                self.tasks.append(Task(taskArr[0],taskArr[1],taskArr[2]))
                                self.taskUpdateLock.release()
