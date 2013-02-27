import time


class Clock(object):
	""" Class to manage time """

	lastTime = 0
	factor = 1
	elapsedTime = 0
	run = True

	def __init__(self):
		self.reset()

	def start(self):
		self.run = True

	def stop(self):
		self.run = False
		self.reset(self)

	def reset(self):
		self.lastTime = time.clock()
		self.elapsedTime = 0

	def pause(self):
		self.run = False

	def getFactor(self):
		return self.factor

	def setFactor(self, factor):
		self.getTime()
		self.factor = factor

	def getTime(self):
		currentTime = time.clock()
		if self.run:
			self.elapsedTime += (currentTime - self.lastTime) * self.factor
		self.lastTime = currentTime
		return self.elapsedTime

if __name__ == "__main__":
	clock = Clock()
	clock.setFactor(1.5)
	while(True):
		print(clock.getTime())
		if(clock.getTime() > 2):
			clock.reset()
