
from math import sqrt, atan2, sin, cos, acos, radians, degrees

from utils import Vector3D


class Leg(object):
	

	def __init__(self, head=0, joint=0, tip=0, bot_position=0, phi=0, bot=None, inverse=False):
		self._bot = bot
		self.motors = (head, joint, tip)
		self.bot_position = bot_position
		self.bot_angle = phi
		self.alphaFactor = 1
		self.gammaFactor = -1
		self.betaFactor = 1



	@property
	def bot(self):
		return self._bot

	@property
	def references(self):
		return self._references

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
		return tuple(motor.position for motor in self.motors)

	def apply_raw_pose(self, raw_pose):
		"docstring"

		print("moving", tuple(motor.position - value for value, motor in zip(raw_pose, self.motors)))

		for value, motor in zip(raw_pose, self.motors):
			motor.compliant = False
			motor.position = value

	def calibration(self):
		self._references = self.raw_pose()

	def pose(self):
		"returns leg's pose and return the motors position according to our calibration references"
		return tuple(value - reference for value, reference in zip(self.raw_pose(), self.references))

	def apply_pose(self, pose):
		"docstring"
		for value, motor, reference in zip(pose, self.motors, self.references):
			motor.position = reference + value

	def position(self):
		a1, a2, b, c = self.sizes

		alpha = self.alphaFactor * radians(self.motors[0].position - self.references[0])
		beta =	self.betaFactor  * radians(self.motors[1].position - self.references[1])
		gamma = self.gammaFactor * radians(self.motors[2].position - self.references[2])

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
		x, y, z = position

		try:
			#
			# Compute alpha
			#
			u = sqrt(x ** 2 + y ** 2)
			if u != 0:
				alpha = atan2(y, x)
			else:
				raise Exception("u impossible")

			alpha = self.alphaFactor * alpha;

			#
			# Compute gamma
			#
			d = (u - a1) ** 2 + (z - a2) ** 2
			if d > (b + c) ** 2 and d < (b - c) ** 2:
				raise Exception("Mouvement impossible")

			gamma = self.gammaFactor * acos((d - b ** 2 - c ** 2) / (2 * b * c))


			#
			# Compute beta
			#
			sin_beta = ((z - a2) * (b + c * cos(gamma)) - (u - a1) * c * sin(gamma)) / ((u - a1) ** 2 * (z - a2) ** 2)
			cos_beta = ((u - a1) * (b + c * cos(gamma)) + (z - a1) * c * sin(gamma)) / ((u - a1) ** 2 * (z - a2) ** 2)

			beta = self.betaFactor * atan2(sin_beta, cos_beta)

			return (degrees(alpha), degrees(beta), degrees(gamma))

		except Exception as e :
			print u
			raise e

	def move(self, position):
		alpha, beta, gamma = self.inverse_model(position)
		self.motors[0].position = self.references[0] + alpha
		self.motors[1].position = self.references[1] + beta
		self.motors[2].position = self.references[2] + gamma
		print(alpha,"|",beta,"|",gamma)

	def bot_move(self, position):
		"""
		Move to position in Bot base.
		
		Rotation Matrix:
			| cos(phi)  sin(phi) 0 |
			| -sin(phi) cos(phi) 0 |
			| 0         0        1 |
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
