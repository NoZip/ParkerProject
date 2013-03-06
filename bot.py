
from leg import Leg


class Bot(object):
	"""
	An Hexapod

	Properties:
		(readonly) legs: Hexapod legs.
		legs_references: results of bot calibration.
	"""

	def __init__(self, control, legs, legs_references, legs_sizes):
		self._control = control

		self._legs = tuple(legs)
		for leg in self._legs:
			leg._bot = self

		self.legs_references = legs_references
		self.legs_sizes = legs_sizes

		self.current_index = 0
		self.current_pose_index = 0
		self.current_pose_move = []
		self.current_move = []

	@property
	def control(self):
		return self._control

	@property
	def legs(self):
		return self._legs

	def _get_compliant(self):
		return all(leg.compliant for leg in self.legs)

	def _set_compliant(self, value):
		for leg in self.legs:
			leg.compliant = value

		self.control.wait(10)


	compliant = property(_get_compliant, _set_compliant)

	def _get_led(self):
		return all(leg.led for leg in self.legs)

	def _set_led(self, value):
		for leg in self.legs:
			leg.led = value

	led = property(_get_led, _set_led)

	def set_move(self, new_move):
		"set a new move for the bot and reset the current_index"
		self.current_move = new_move
		self.current_index = 0

	def set_pose_move(self, new_move):
		"set a new move for the bot and reset the current_index"
		self.current_pose_move = new_move
		self.current_pose_index = 0

	def play_move(self):
		"play the current move and increment the current_index"

		for leg, position in zip(self.legs, self.current_move[self.current_index]):
			leg.move(position)

		self.current_index = (self.currentIndex + 1) % len(self.current_move)

	def play_pose_move(self):
		for leg, position in zip(self.legs, self.current_pose_move[self.current_pose_index]):
			leg.apply_raw_pose(position)

		self.current_pose_index = (self.current_pose_index + 1) % len(self.current_pose_move)

	def apply_raw_pose(self, pose):
		"Apply a raw_pose to the whole bot"

		for leg, leg_pose in zip(self.legs, pose):
			leg.apply_raw_pose(leg_pose)

	def apply_pose(self, pose):
		"Apply a pose to the whole bot"

		for leg, leg_pose in zip(self.legs, pose):
			leg.apply_pose(leg_pose)

	def pose(self):
		"return a list with the 6 legs poses"
		return tuple(leg.pose() for leg in self.legs)

	def raw_pose(self):
		"return a list with the 6 legs raw_pose"
		return tuple(leg.raw_pose() for leg in self.legs)

	def _move_legs(self, legs_ids, positions, inverse_model=False):
		"""
		Move a set of legs to a position
		EXPERIMENTAL!
		"""
		assert(len(legs_ids) == len(positions))

		references = self.legs_references

		if inverse_model:
			positions = tuple(self.legs[0].inverse_model(position) for position in positions)
		print(positions)

		for motor_id, motor_positions in enumerate(zip(*positions)):
			for i, motor_position in enumerate(motor_positions):
				self.legs[legs_ids[i]].motors[motor_id].position = references[motor_id] + motor_position

			self.control.wait(100)



def Spidey(control):
	"initialize real hexapod"
	legs = [
		Leg(control.motors[0], control.motors[2], control.motors[4]),
		Leg(control.motors[12], control.motors[14], control.motors[16], inverse=True),
		Leg(control.motors[13], control.motors[15], control.motors[17]),
		Leg(control.motors[7], control.motors[9], control.motors[11]),
		Leg(control.motors[1], control.motors[3], control.motors[5], inverse=True),
		Leg(control.motors[6], control.motors[8], control.motors[10], inverse=True)
	]

	a1 = 	5.000
	a2 = 	-4.000
	b  = 	6.500
	c  = 	9.500

	legs_sizes = (a1, a2, b, c)

	legs_references = (148.38709677419354, 161.87683284457478, 88.26979472140764)

	return Bot(control, legs, legs_references, legs_sizes)


def SymbiotSpidey(control):
	"initialize simulation hexapod"
	legs = [
		Leg(control.motors[0], control.motors[1], control.motors[2]),
		Leg(control.motors[3], control.motors[4], control.motors[5]),
		Leg(control.motors[6], control.motors[7], control.motors[8]),
		Leg(control.motors[9], control.motors[10], control.motors[11]),
		Leg(control.motors[12], control.motors[13], control.motors[14]),
		Leg(control.motors[15], control.motors[16], control.motors[17])
	]

	a1 = 	5.000
	a2 = 	-4.000
	b  = 	6.500
	c  = 	9.500

	legs_sizes = (a1, a2, b, c)

	# Calibration needed
	legs_references = (148.38709677419354, 161.87683284457478, 88.26979472140764)

	return Bot(control, legs, legs_references, legs_sizes)
