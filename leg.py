from collections import namedtuple

from math import sqrt, atan, sin, asin, cos, acos, radians, degrees

from utils import Vector3D

class Leg(object):

	a1 = 	5.000
	a2 = 	-4.000
	b  = 	6.500
	c  = 	9.500

	references = (0, 0, 0)
	
	def __init__(self, head, joint, tip, inverse=False):
		self.motors = (head, joint, tip)
		self._inverse = -1 if inverse else 1
	
	def _get_compliant(self):
		return all(motor.compliant for motor in self.motors)

	def _set_compliant(self, value):
		for motor in self.motors:
			motor.compliant = value

	compliant = property(_get_compliant, _set_compliant)

	def _get_led(self):
		return all(motor.led for motor in self.motors)

	def _set_led(self, value):
		for motor in self.motors:
			motor.led = value

	led = property(_get_led, _set_led)

	def raw_pose(self):
		"returns leg's pose and return the motors position raw values"
		for motor in self.motors:
			motor.compliant = False
		return tuple(motor.position for motor in self.motors)

	def apply_raw_pose(self, raw_pose):
		"docstring"

		print("moving", tuple(motor.position - value for value, motor in zip(raw_pose, self.motors)))

		for value, motor in zip(raw_pose, self.motors):
			motor.compliant = False
			motor.position = value

	def calibration(self):
		self.references = self.raw_pose()

	def pose(self):
		"returns leg's pose and return the motors position according to our calibration references"
		return tuple(value - reference for value, reference in zip(self.raw_pose(), self.references))

	def apply_pose(self, pose):
		"docstring"
		print("moving", tuple(motor.position - reference + value for reference, value, motor in zip(self.references, pose, self.motors)))

		for value, motor, reference in zip(pose, self.motors, self.references):
			motor.position = reference + value

	def position(self):
		
		alpha = self._inverse * radians(self.motors[0].position - self.references[0])
		beta = self._inverse * radians(self.motors[1].position - self.references[1])
		gamma = -self._inverse * radians(self.motors[2].position - self.references[2])

		return Vector3D(
			x = cos(alpha) * (self.a1 + self.b * cos(beta) + self.c * cos(beta + gamma)),
			y = sin(alpha) * (self.a1 + self.b * cos(beta) + self.c * cos(beta + gamma)),
			z = self.a2 + self.b * sin(beta) + self.c * sin(beta + gamma)
		)

	@classmethod
	def inverse_model(cls, position):
		print("position =", position)

		# Calcul alpha
		u = sqrt(position.x ** 2 + position.y ** 2)
		print("u =", u)

		alpha = 2 * atan(position.y / (position.x + u ** 2))

		# Calcul gamma (au signe pres)
		cos_gamma = (
			((u - cls.a1) ** 2 + ((position.z - cls.a2) ** 2 - cls.b ** 2 -cls.c ** 2))
			/ (2 * cls.b * cls.c)
		)

		print("cos_gamma =", cos_gamma)

		try :
			gamma = acos(cos_gamma)
		except ValueError as e:
			print(cos_gamma)
			raise e

		#calcul beta
		cos_beta = (
			((u - cls.a1) * (cls.b + cls.c * cos(gamma)) + (position.z - cls.a2) * cls.c * sin(gamma))
			/ ((u - cls.a1) ** 2 + (position.z - cls.a2) ** 2)
		)

		sin_beta = (
			((position.z - cls.a2) * (cls.b + cls.c * cos(gamma)) - (u -cls.a1) * cls.c * sin(gamma))
			/ ((u - cls.a1) ** 2 + (position.z - cls.a2) ** 2)
		)

		print("cos_beta =", cos_beta)
		print("sin_beta =", sin_beta)

		try :
			beta = acos(cos_beta)
		except ValueError as e:
			print(cos_beta)
			raise e

		print("alpha =", degrees(alpha))
		print("beta =", degrees(beta))
		print("gamma =", degrees(gamma))

		return (degrees(alpha), degrees(beta), degrees(gamma))

	def move(self, position):
		alpha, beta, gamma = self.inverse_model(position)

		self.motors[0].position = (self._inverse * (self.references[0] + alpha)) % 300
		self.motors[1].position = (self._inverse * (self.references[1] + beta)) % 300
		self.motors[2].position = (self._inverse * (self.references[2] + gamma)) % 300

	def animate(self, f_animation):
		#while(time < duration)
		#...
		#self.head.position = f_animation(self, time);
		#...
		pass