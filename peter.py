from collections import namedtuple

from math import sin, cos, radians

Vector3D = namedtuple("Vector3D", ("x", "y", "z"))

Move = tuple

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

	property(_get_compliant, _set_compliant)

	def _get_led(self):
		return all(motor.led for motor in self.motors)

	def _set_led(self, value):
		for motor in self.motors:
			motor.led = value

	property(_get_led, _set_led)

	def raw_pose(self):
		"returns leg's pose and return the motors position raw values"
		for motor in self.motors:
			motor.compliant = True

		raw_input("Press ENTER when the pose is ready ...")

		pose = tuple(motor.position for motor in self.motors)

		for motor in self.motors:
			motor.compliant = False

		return pose

	def apply_raw_pose(self, raw_pose):
		"docstring"
		for value, motor in zip(pose, self.motors):
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


class Bot(object):
	"Spidey"

	currentMove = [Move(Vector3D(0,0,0),Vector3D(0,0,0),Vector3D(0,0,0),Vector3D(0,0,0),Vector3D(0,0,0),Vector3D(0,0,0))] 
	#Array of Move (One move == 6 positions)
	currentIndex = 0
	#Index in the current move, used in the play func

	def __init__(self, legs):
		self.legs = legs

	def setMove(self, newMove):
		"set a new move for the bot and reset the currentIndex"
		self.currentMove = newMove
		self.currentIndex = 0

	def playMove(self):
		"play the current move and increment the currentIndex"
		for i in xrange(0,self.legs.len()):
			self.legs[i].position(self.currentMove[currentIndex][i])


def Spidey(control):
	legs = [
		Leg(control.motors[0], control.motors[2], control.motors[4])
		Leg(control.motors[12], control.motors[14], control.motors[16]),
		Leg(control.motors[13], control.motors[15], control.motors[17]),
		Leg(control.motors[7], control.motors[9], control.motors[11]),
		Leg(control.motors[1], control.motors[3], control.motors[5]),
		Leg(control.motors[6], control.motors[8], control.motors[10]),
	]

	return Bot(legs)