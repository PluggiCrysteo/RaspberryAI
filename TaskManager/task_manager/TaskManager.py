#! /usr/bin/python

import logging,time,threading,os,sys

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
		taskUpdaterThread = threading.Thread(target=self.readNamedPipe)
		taskUpdaterThread.start()
		
		logger.info("starting the loop (executing tasks)")
		while(True):
			time.sleep(0.5)
			if not self.tasks:		## no need to keep going if lsit is empty
				continue
				
			logger.debug("tasks was not empty")
			
			self.taskUpdateLock.acquire()			## aint modifying tasks
			
			if self.tasks[0].state == Task.FINISHED:		## popping finished task
				self.tasks[0].pop(0)
				
			self.tasks.sort(key= lambda x : x.value, reverse = True)	## ordering tasks to get the best one
			
			if tasks[0].state == Task.NOT_STARTED:			### starting / resuming the task we have to do
				tasks[0].start()
			elif tasks[0].state == Task.STARTED:
				tasks[0].resume()
				
			self.taskUpdateLock.release()		## release lock, can be interupted again

	def readNamedPipe(self):
		with open(self.fifoPath, 'r',0) as fifo_read:
			logger.debug("opened the reading-end of the caca fifo")
			while(True):
			        line = fifo_read.readline()
	        		print line
		        	logger.debug("reading a line")
				taskArr = str.split(str=";", num=string.count(str))
				self.taskUpdateLock.acquire()
				self.tasks.append(Task(taskArr[0],taskArr[1],None))
				self.taskUpdateLock.release()


