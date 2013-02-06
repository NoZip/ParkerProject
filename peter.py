from collections import namedtuple

from math import sin, cos, radians

Vector3D = namedtuple("Vector3D", ("x", "y", "z"))

class Leg(object):

	a1 = 	5.000
	a2 = 	-4.000
	b = 	6.500
	c = 	9.500

	references = (0, 0, 0)
	
	def __init__(self, head, joint, tip):
		self.motors = [head, joint, tip]
	
	def raw_pose(self):
		"returns leg's pose and return the motors position raw values"
		for motor in self.motors:
			motor.compliant = True

		raw_input("Press ENTER when the pose is ready ...")

		pose = tuple(motor.position for motor in self.motors)

		for motor in self.motors:
			motor.compliant = False

		return pose

	def calibration(self):
		self.references = self.pose()

	def pose(self):
		"returns leg's pose and return the motors position according to our calibration references"
		return tuple(value - reference for value, reference in zip(self.raw_pose(), self.references))

	def position(self):
		alpha = radians(self.motors[0].position - self.references[0])
		beta = radians(self.motors[1].position - self.references[1])
		gamma = -radians(self.motors[2].position - self.references[2])

		# xa = 0
		# ya = 0
		# za = 0

		# x = xa + self.a1 * cos(alpha)
		# y = ya + self.a2 * sin(alpha)
		# z = za 

		#return Vector3D(alpha, beta, gamma)
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
