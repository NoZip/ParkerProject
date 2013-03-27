import sys

import pydyn.dynamixel as dyn

from utils import Vector3D
from bot import Spidey, SymbiotSpidey
from leg import Leg


def init_ctrl():
	"""motors initialisation"""
	if len(sys.argv) == 2:
		min_id, max_id = int(sys.argv[0]), int(sys.argv[1])
	else:
		min_id, max_id = 0, 26

	ctrl = dyn.create_controller(verbose = True, motor_range = [min_id, max_id])
	sys.stdout.flush()
	return ctrl

def test(simulation=False):
	"""test of inverse model"""
	simulation = False
	if simulation:
		dyn.enable_vrep()
	
	ctrl = init_ctrl()

	if simulation:
		peter = SymbiotSpidey(ctrl)
	else:
		peter = Spidey(ctrl)

	if simulation:
		ctrl.start_sim()

	peter.compliant = False
	ctrl.wait(10)

	for leg in peter.legs:
		leg.move(Vector3D(1, 4, 0))
		ctrl.wait(100)

	peter.compliant = True
	ctrl.wait(10)

	if simulation:
		ctrl.stop_sim()


if __name__ == "__main__":
	test(simulation=True)