import time

class Clock(object):
	"""To manage time"""

	def __init__(self):
		self.currentTime = 0
		self.lastTime = time.clock()
		self.timeBuffer = self.lastTime
	
	def start():
		self.lastTime = time.clock()
		pass

	@property
	def time():
		computeTime()
		return currentTime

	def computeTime() :
		currentTime = time.clock()
		timeBuffer += currentTime-lastTime
		lastTime = currentTime