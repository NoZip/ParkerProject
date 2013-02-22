
from leg import Leg
from utils import Vector3D


class Bot(object):
	"An Hexapod"

	def __init__(self, legs):
		self.legs = legs
		self.current_index = 0
		self.current_move = []

	def _get_compliant(self):
		return all(leg.compliant for leg in self.legs)

	def _set_compliant(self, value):
		for leg in self.legs:
			leg.compliant = value

	compliant = property(_get_compliant, _set_compliant)

	def _get_led(self):
		return all(leg.led for leg in self.legs)

	def _set_led(self, value):
		for leg in self.legs:
			leg.led = value

	led = property(_get_led, _set_led)

	def setMove(self, newMove):
		"set a new move for the bot and reset the current_index"
		self.current_move = newMove
		self.current_index = 0

	def playMove(self):
		"play the current move and increment the current_index"

		for leg, pose in zip(self.legs, self.current_move[self.current_index]):
			leg.apply_raw_pose(pose)

		self.current_index += 1

	def pose(self):
		"return a list with the 6 legs"
		return tuple(leg.raw_pose() for leg in self.legs)


def Spidey(control):
	"initialize real hexapod"
	legs = [
		Leg(control.motors[0], control.motors[2], control.motors[4]),
		Leg(control.motors[12], control.motors[14], control.motors[16], True),
		Leg(control.motors[13], control.motors[15], control.motors[17]),
		Leg(control.motors[7], control.motors[9], control.motors[11]),
		Leg(control.motors[1], control.motors[3], control.motors[5], True),
		Leg(control.motors[6], control.motors[8], control.motors[10], True)
	]

	return Bot(legs)