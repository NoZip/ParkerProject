class Leg(object):
	def __init__(self, head, joint, tip):
		self.motors = [head, joint, tip]

	def calibration(self):
		self.reference = {}

		for motor in self.motors:
			motor.compliant = True

		raw_input("Press ENTER when the pose is ready ...")

		for motor in self.motors:
			self.reference[motor] = motor.position

		for motor in self.motors:
			motor.compliant = False

		print self.reference

	def position(self):
		pass

	def move(position):
		pass

	def animate(self, f_animation):
		#while(time < duration)
		#...
		#self.head.position = f_animation(self, time);
		#...
		pass


class Peter(object):
	"Spidey"

	def __init__(self, control):
		pass