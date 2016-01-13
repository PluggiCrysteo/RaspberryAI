class Task:
	def __init__(self, priority, cost, action):
		self.priority = priority
		self.cost = cost
		self.value = priority - cost
		self.action = action
		print "Instantiated a task with a priority of " + priority
		print " a cost of : " + cost
		
	def getAction():
		return self.action
