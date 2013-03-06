import sys

import pydyn.dynamixel as dyn

from bot import Spidey, SymbiotSpidey


def init_ctrl():
	"""motors initialisation"""
	if len(sys.argv) == 2:
		min_id, max_id = int(sys.argv[0]), int(sys.argv[1])
	else:
		min_id, max_id = 0, 26

	ctrl = dyn.create_controller(verbose = True, motor_range = [min_id, max_id])
	sys.stdout.flush()
	return ctrl

def calibration(simulation=False):
	"""calibration"""
	if simulation:
		dyn.enable_vrep()
	
	ctrl = init_ctrl()

	if simulation:
		peter = SymbiotSpidey(ctrl)
	else:
		peter = Spidey(ctrl)

	if simulation:
		ctrl.start_sim()

	peter.compliant = True
	ctrl.wait(10)

	leg = peter.legs[0]
	leg.led = True
	ctrl.wait(10)

	raw_input("Calibration. Press enter when done...")

	peter.compliant = False
	ctrl.wait(10)

	references = (motor.position for motor in leg.motors)
	print("references :", references)

	if simulation:
		ctrl.stop_sim()


if __name__ == "__main__":
	calibration(simulation=True)