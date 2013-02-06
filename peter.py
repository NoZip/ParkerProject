from collections import namedtuple

from math import sin, cos

Vector3D = namedtuple("Vector3D", ("x", "y", "z"))

class Leg(object):

	a1 = 4.5
	a2 = 3.9
	b = 6.5
	c = 9.5

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

		print(self.references)

	def position(self):
		alpha = self.motors[0].position - self.references[0]
		beta = self.motors[1].position - self.references[1]
		gamma = self.motors[2].position - self.references[2]

		return Vector3D(
			x = cos(alpha) * (self.a1 + self.b * cos(beta) + self.c * cos(beta + gamma)),
			y = sin(alpha) * (self.a1 + self.b * cos(beta) + self.c * cos(beta + gamma)),
			z = self.a2 + self.b * sin(beta) + self.c * sin(beta + gamma)
		)

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
