
from math import sqrt, atan, sin, cos, acos, radians, degrees

from utils import Vector3D


class Leg(object):

	def __init__(self, head, joint, tip, bot_position, phi, bot=None, inverse=False):
		self._bot = bot
		self.motors = (head, joint, tip)
		self.bot_position = bot_position
		self.bot_angle = phi
		self._inverse = -1 if inverse else 1

	@property
	def bot(self):
		return self._bot

	@property
	def references(self):
		return self._bot.legs_references

	@property
	def sizes(self):
		return self._bot.legs_sizes

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
		for value, motor, reference in zip(pose, self.motors, self.references):
			motor.position = reference + value

	def position(self):

		a1, a2, b, c = self.sizes

		alpha = self._inverse * radians(self.motors[0].position - self.references[0])
		beta = self._inverse * radians(self.motors[1].position - self.references[1])
		gamma = -self._inverse * radians(self.motors[2].position - self.references[2])

		return Vector3D(
			x = cos(alpha) * (a1 + b * cos(beta) + c * cos(beta + gamma)),
			y = sin(alpha) * (a1 + b * cos(beta) + c * cos(beta + gamma)),
			z = a2 + b * sin(beta) + c * sin(beta + gamma)
		)

	def bot_position(self):
		"""
		Position in Bot base.
		
		Rotation Matrix:
			| cos(phi) -sin(phi) 0 |
			| sin(phi) cos(phi)  0 |
			| 0        0         1 |
		"""
		phi = self.bot_angle
		x, y, z = self.position()

		return Vector3D(
			x = x * cos(phi) - y * sin(phi) + bot_position.x,
			y = y * cos(phi) + x * sin(phi) + bot_position.y,
			z = z + bot_position.z
		)

	def inverse_model(self, position):
		a1, a2, b, c = self.sizes

		# Calcul alpha
		u = sqrt(position.x ** 2 + position.y ** 2)

		alpha = 2 * atan(position.y / (position.x + u ** 2))

		# Calcul gamma (au signe pres)
		cos_gamma = (
			((u - a1) ** 2 + ((position.z - a2) ** 2 - b ** 2 - c ** 2))
			/ (2 * b * c)
		)

		try:
			gamma = acos(cos_gamma)
		except ValueError as e:
			print("cos_gamma =", cos_gamma)
			raise e

		#calcul beta
		cos_beta = (
			((u - a1) * (b + c * cos(gamma)) + (position.z - a2) * c * sin(gamma))
			/ ((u - a1) ** 2 + (position.z - a2) ** 2)
		)

		sin_beta = (
			((position.z - a2) * (b + c * cos(gamma)) - (u - a1) * c * sin(gamma))
			/ ((u - a1) ** 2 + (position.z - a2) ** 2)
		)

		try:
			beta = acos(cos_beta)
		except ValueError as e:
			print("cos_beta =", cos_beta)
			print("sin_beta =", sin_beta)
			raise e

		return (degrees(alpha), degrees(beta), degrees(gamma))

	def move(self, position):
		alpha, beta, gamma = self.inverse_model(position)

		self.motors[0].position = (self._inverse * (self.references[0] + alpha)) % 300
		self.motors[1].position = (self._inverse * (self.references[1] + beta)) % 300
		self.motors[2].position = (self._inverse * (self.references[2] + gamma)) % 300

	def bot_move(self, position):
		"""
		Move to position in Bot base.
		
		Rotation Matrix:
			| cos(phi)  sin(phi) 0 |
			| -sin(phi) cos(phi) 0 |
			| 0        0         1 |
		"""

		phi = self.bot_angle
		x, y, z = position

		leg_position = Vector3D(
			x = x * cos(phi) + y * sin(phi) - bot_position.x,
			y = y * cos(phi) - x * sin(phi) - bot_position.y,
			z = z - bot_position.z
		)

		self.move(leg_position)

	def animate(self, f_animation):
		#while(time < duration)
		#...
		#self.head.position = f_animation(self, time);
		#...
		pass
