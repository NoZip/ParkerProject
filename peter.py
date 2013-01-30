class Leg(object):
	references = [0, 0, 0]
	
	def __init__(self, head, joint, tip):
		self.motors = [head, joint, tip]

	def calibration(self):
		for motor in self.motors:
			motor.compliant = True

		raw_input("Press ENTER when the pose is ready ...")

		for i, motor in enumerate(self.motors):
			self.references[i] = motor.position

		for motor in self.motors:
			motor.compliant = False

		print self.references

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
