from collections import namedtuple

from math import sin, cos, radians

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
			motor.led = True
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

	def move(self, position):
		self.motor[0].position = atan2(position.y, position.x)

	def animate(self, f_animation):
		#while(time < duration)
		#...
		#self.head.position = f_animation(self, time);
		#...
		pass