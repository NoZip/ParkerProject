import sys
import time
import math
import pydyn.dynamixel as dyn
from utils import *
from bot import *
from pose import *
from move import *
#from clock import Clock
from setup import *
import json


def main():
	ctrl = initCtrl()
	peter = Spidey(ctrl)
	move(peter, (0, 0))

	# drawSquareMode(ctrl)

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
	# Leg.references = (148.38709677419354, 161.87683284457478, 88.26979472140764)
	# peter.led = True
	
##########################################################################################

	# ctrl = initCtrl()
	# peter = Spidey(ctrl)
	# if len(sys.argv) == 2:
	# 	poseFilename = sys.argv[1]
	# 	poseFile = open(poseFilename, 'r')
	# 	poses = json.loads(poseFile.read())
	# 	raw_input("Press ENTER to play the moves")
	# 	peter.set_pose_move(poses)
	# 	while peter.current_pose_index < len(poses)-1:
	# 		peter.play_pose_move()
	# 		ctrl.wait(10)
	# 	peter.play_pose_move()
	# 	ctrl.wait(10)
	# else:
	# 	poseFilename = "tmp.move"
	# 	poseFile = open(poseFilename, 'w')
	# 	poses = []
	# 	while(raw_input("Press ENTER to continue or S to stop ...") != 's'):
	# 		peter.compliant = True
	# 		raw_input("Press ENTER to confirm the pose ...")
	# 		peter.compliant = False
	# 		poses.append(peter.raw_pose())
	# 	poseFile.write(json.dumps(poses))
	# 	poseFile.close()
	# peter.compliant = True
	# ctrl.wait(1)

##########################################################################################

	# peter.compliant = False
	# raw_input("ENTER to play the move for a long time")
	# peter.set_pose_move(poses)

	# while True:
	# 	peter.play_pose_move()
	# 	ctrl.wait(5)

	# ctrl.wait(5)


def initCtrl():
	min_id, max_id = 0, 20
	ctrl = dyn.create_controller(verbose=True, motor_range=[min_id, max_id], timeout=0.05)
	for motor in ctrl.motors:
		motor.max_torque = 50
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

def drawSquareMode(ctrl):
	peter = Spidey(ctrl)
	setMotorsCompliant(ctrl, False)
	positions = [Vector3D(0,3,3),Vector3D(0,3,6),Vector3D(0,6,6),Vector3D(0,6,3)]
	frame = 0
	while 1 :
		print "a"
		peter.legs[0].move(positions[frame%4])
		frame += 1
		ctrl.wait(10)


if __name__ == "__main__":
	main()
