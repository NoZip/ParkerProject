
from leg import Leg
from utils import Vector3D

Move = tuple

class Bot(object):
	"Spidey"

	currentMove = [({},{},{},{},{},{})] 
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

	def pose(self):
		"return a list with the 6 legs"
		positions={}
		for leg in self.legs:
			positions.append(leg.pose())
		return positions


def Spidey(control):
	legs = [
		Leg(control.motors[0], control.motors[2], control.motors[4]),
		Leg(control.motors[12], control.motors[14], control.motors[16], True),
		Leg(control.motors[13], control.motors[15], control.motors[17]),
		Leg(control.motors[7], control.motors[9], control.motors[11]),
		Leg(control.motors[1], control.motors[3], control.motors[5], True),
		Leg(control.motors[6], control.motors[8], control.motors[10], True)
	]

	return Bot(legs)