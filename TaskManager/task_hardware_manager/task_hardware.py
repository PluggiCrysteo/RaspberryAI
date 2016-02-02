import logging

class Task:

	NOT_STARTED = 0
	STARTED = 1
	PAUSED = 2
	FINISHED = 3
	logger = logging.getLogger("TaskManager")
	
	def __init__(self, priority, cost, action):
		self.priority = int(priority)
		self.cost = int(cost)
		self.value = self.priority - self.cost
		self.action = action
		self.state = self.NOT_STARTED
		self.logger.debug("Instantiated a task with a priority of " + priority)
		self.logger.debug(" a cost of : " + cost)
		self.logger.debug("and the task is: " + action)
		
	def get_action(self):
		return self.action
		
	def pause(self):
		self.logger.debug("Pausing a task")
		
	def start(self):
		self.state = self.STARTED
		if self.state == self.PAUSED:
			self.resume()
		else:
			self.logger.debug("Starting a task")
		
	def resume(self):
		self.logger.debug("Resuming a task")
