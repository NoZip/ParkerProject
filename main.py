import sys
import time
import math
import pydyn.dynamixel as dyn
from utils import *
from bot import *
from pose import *
#from clock import Clock
from setup import *


def main():

	ctrl = initCtrl()
	# setupHW = None;
	# setupSW = None;

	# # dyn.enable_vrep()
	# ctrl = initCtrl()
	# setupHW = botSetup(ctrl, False)

	# dyn.enable_vrep()
	# ctrl = initCtrl()
	# setupSW = botSetup(ctrl, True)

	# idsHW = setupHW[0]
	# factorsHW = setupHW[1]
	# referenceHW = setupHW[2]
	# idsSW = setupSW[0]
	# factorsSW = setupSW[1]
	# referenceSW = setupSW[2]
	# for i in range(len(idsHW)) :
	# 	print i ," : ", referenceHW[idsHW[i]] ,"-", referenceSW[idsSW[i]] ," = ", referenceHW[idsHW[i]]-referenceSW[idsSW[i]]

	poses = []
	Leg.references = (148.38709677419354, 161.87683284457478, 88.26979472140764)

	peter = Spidey(ctrl)

	# peter.led = True

	while(raw_input("Press ENTER when the pose is ready ...") != 's'):
		peter.compliant = True
		raw_input("Confirm POSE NOW !")
		peter.compliant = False
		poses.append(peter.pose())
		peter.compliant = True

	# myFile = open('walk.move', 'w')
	# myFile.write(poses)
	# myFile.close()

	print(poses)

	peter.compliant = False
	raw_input("ENTER to play the move for a long time")
	peter.set_pose_move(poses)

	while True:
		peter.play_pose_move()
		ctrl.wait(20)

	ctrl.wait(5)


def initCtrl():
	if len(sys.argv) == 2:
		min_id, max_id = int(sys.argv[1]), int(sys.argv[1])
	else:
		min_id, max_id = 0, 20

	ctrl = dyn.create_controller(verbose = True, motor_range = [min_id, max_id])
	sys.stdout.flush()
	return ctrl


def setMotorsCompliant(ctrl, compliant):
	for motor in ctrl.motors:
		motor.compliant = compliant


def poseMode(ctrl):
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


def toggleCompliantMode(ctrl):
	compliant = True
	while True:
		compliant = not(compliant)
		setMotorsCompliant(ctrl, compliant)
		print("Set motors to compliant = ", compliant)
		raw_input("Press ENTER To toggle compliant ...")


def sinAnimationMode(ctrl):
	startTime = time.clock()
	maxTime = 10
	currentTime = startTime

	while(currentTime-startTime < maxTime):
		currentTime = time.clock()
		elapsedTime = currentTime-startTime

		for m in ctrl.motors:
			m.led = True
			m.position = 80 + math.sin(elapsedTime) * 30

if __name__ == "__main__":
	main()
