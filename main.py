import sys, time, math
import pydyn.dynamixel as dyn
from utils import *
from bot import *
from pose import *
from clock import Clock

def main() :

	# dyn.enable_vrep()
	ctrl = initCtrl()

	poses = []

	Leg.references = (148.38709677419354, 161.87683284457478, 88.26979472140764)

	peter = Spidey(ctrl)

	peter.led = True
	peter.compliant = True

	raw_input("Press ENTER when the pose is ready ...")

	peter.compliant = False

	poses.append(peter.pose())

	peter.compliant = True

	# print(poses)
	raw_input("Press ENTER when ready ...")

	peter.compliant = False

	peter.set_move(poses)
	peter.play_move()
	ctrl.wait(5)

def initCtrl() :
	if len(sys.argv) == 2:
	    min_id, max_id = int(sys.argv[1]), int(sys.argv[1])
	else:
	    min_id, max_id = 0, 253

	ctrl = dyn.create_controller(verbose = True, motor_range = [min_id, max_id])
	sys.stdout.flush()
	return ctrl

def poseMain(ctrl) :
	# Let the user set up the pose
	setMotorsCompliant(ctrl, True)
	raw_input("Press ENTER when the pose is ready ...")
	setMotorsCompliant(ctrl, False)

	pose = savePose(ctrl)

	setMotorsCompliant(ctrl, True)
	raw_input("Press ENTER when the pose is gone ...")
	setMotorsCompliant(ctrl, False)

	applyPose(ctrl, pose)

	return pose

def setMotorsCompliant(ctrl, compliant) :
	for motor in ctrl.motors:
		motor.compliant = compliant;

def sinAnimation(ctrl) : 
	startTime = time.clock()
	maxTime = 10
	currentTime = startTime

	while(currentTime-startTime < maxTime) :
		currentTime = time.clock();
		elapsedTime = currentTime-startTime

		for m in ctrl.motors:
			m.led = True
			m.position = 80 + math.sin(elapsedTime) * 30;

if __name__ == "__main__":
	main()