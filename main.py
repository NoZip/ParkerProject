import sys, time, math
import pydyn.dynamixel as dyn
from peter import Leg
from pose import *
from clock import Clock

def main() :
	ctrl = initCtrl()

	#poseMain(ctrl)

	leg = Leg(ctrl.motors[1], ctrl.motors[3], ctrl.motors[5])
	leg.references = (148.38709677419354, 161.87683284457478, 88.26979472140764)

	print("references", leg.references)
	print("raw_pose", leg.raw_pose())
	print("pose", leg.pose())
	setMotorsCompliant(ctrl, True)
	
	poses = []
	raw_input("point 1 ...")
	poses += [savePose(ctrl, [1,3,5])]
	raw_input("point 2 ...")
	poses += [savePose(ctrl, [1,3,5])]
	raw_input("point 3 ...")
	poses += [savePose(ctrl, [1,3,5])]
	raw_input("point 4 ...")
	poses += [savePose(ctrl, [1,3,5])]

	setMotorsCompliant(ctrl, False)

	clock = Clock()
	while clock.getTime() < 4 :
		pose = int(math.floor(clock.getTime()))
		applyPose(ctrl, poses[pose])
	print 'done'

	#applyPose(ctrl, {1 : 148.38709677419354, 3 : 161.87683284457478, 5 : 88.26979472140764})

	setMotorsCompliant(ctrl, True)

	ctrl.wait(2)

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

main()