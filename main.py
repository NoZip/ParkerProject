import sys, time, math
import pydyn.dynamixel as dyn
from peter import Leg

def main() :
	if len(sys.argv) == 2:
	    min_id, max_id = int(sys.argv[1]), int(sys.argv[1])
	else:
	    min_id, max_id = 0, 253

	ctrl = dyn.create_controller(verbose = True, motor_range = [min_id, max_id])

	sys.stdout.flush();
	print 'start'

	# # Compliant setup loop
	# for m in ctrl.motors:
	# 	m.compliant = False;

	# pose = display_pose(ctrl)

	# # Compliant setup loop
	# for m in ctrl.motors:
	# 	m.compliant = True;


	# raw_input("Press ENTER when the pose is ready ...")

	# apply_pose(ctrl, pose)

	# # Compliant setup loop
	# for m in ctrl.motors:
	# 	m.compliant = True;

	leg = Leg(ctrl.motors[1], ctrl.motors[3], ctrl.motors[5])
	leg.calibration()

	ctrl.wait(2)
	print 'done'


def display_pose(ctrl) :
	# Compliant setup loop
	for m in ctrl.motors:
		m.compliant = True;

	raw_input("Press ENTER when the pose is ready ...")

	for m in ctrl.motors:
		m.compliant = False;

	pose = {}
	for m in ctrl.motors:
		pose[m.id] = m.position

	print pose
	return pose

def apply_pose(ctrl, pose) :
	print "applying"
	for m in ctrl.motors:
		m.position = pose[m.id]

def sinAnimation(ctrl) : 
	startTime = time.clock()
	maxTime = 10
	currentTime = startTime

	while(currentTime-startTime < maxTime) :
		currentTime = time.clock();
		elapsedTime = currentTime-startTime

		for m in ctrl.motors:
			m.led = True
			#print(m.id, m.position, m.position_raw) 
			m.position = 80 + math.sin(elapsedTime) * 30;

main()