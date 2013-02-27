

def savePose(ctrl, motorIds = []):
	pose = {}
	if not motorIds:
		for i in range(len(ctrl.motors)):
			pose[motorIds[i]] = ctrl.motors[motorIds[i]].position
	else:
		for index in motorIds:
			pose[index] = ctrl.motors[index].position
	return pose


def applyPose(ctrl, pose):
	for k, v in pose.items():
		ctrl.motors[k].position = v
