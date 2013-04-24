import time, sys
import pydyn

import kin
import spiders

ctrl = pydyn.dynamixel.create_controller(motor_range=[0, 20], verbose = True)
spido = spiders.SpiderInterface(ctrl)



for leg in spido.legs:
    leg.compliant = False
    leg.position  = 150, 150, 150


time.sleep(1.0)

# 150.0, 60.0,  60.0,
# 150.0, 240.0, 240.0
# spido.legs[2].position = 150,240,240
# spido.legs[0].position = 150,60,60
spido.spread(30)

time.sleep(1.0)

speed = 0.50

proximal_pose = (150-30, 150, 150+30, 150-30, 150, 150+30)


for motor in ctrl.motors:
		motor.max_torque = 50

while 1:

	####FRAME 1#####
	for leg in spido.legs:
	    if leg.number % 2 == 0:
	    	leg.displace_tip(0,  0, -60)
	    else:
	    	leg.displace_tip(10,  60, 0)

	time.sleep(speed)

	for leg in spido.legs:
	    leg.position  = 150, 150, 150
	    spido.spread(30)

	time.sleep(speed)

	####FRAME 2#####
	for leg in spido.legs:
	    if leg.number % 2 == 0:
	    	leg.displace_tip(10,  60, 0)
	    else:
	    	leg.displace_tip(0,  0, -60)
	time.sleep(speed)

	for leg in spido.legs:
	    leg.position  = 150, 150, 150
	    spido.spread(30)

	time.sleep(speed)

	####FRAME 3#####
	for leg in spido.legs:
	    if leg.number % 2 == 0:
	    	leg.displace_tip(0,  0, -60)
	    else:
	    	leg.displace_tip(10,  60, 0)
	time.sleep(speed)

	for leg in spido.legs:
	    leg.position  = 150, 150, 150
	    spido.spread(30)

	time.sleep(speed)


	# for leg in spido.legs:
	#     if leg.number % 2 == 0:
	#     	leg.displace_tip(0,  0, 60)
	#     else:
	#     	leg.displace_tip(0,  , 0)

	# time.sleep(speed)

	# for leg in spido.legs:
	#     if leg.number % 2 == 0:
	#     	leg.displace_tip(0,  0, 60)
	#     else:
	#     	leg.displace_tip(0,  0, 0)

	# time.sleep(speed)

	# for p_i, leg in zip(proximal_pose, spido.legs):
	# 	if leg.number % 2 == 0:
	# 		leg.position  = 150, 150, 150
	# 		leg.proximo.position = p_i

	# time.sleep(speed)

	# for leg in spido.legs:
	#     if leg.number % 2 != 0:
	#     	leg.displace_tip(0,  0, -60)
	#     else:
	#     	leg.displace_tip(0,  0, 0)
	# time.sleep(speed)

	# for leg in spido.legs:
	#     if leg.number % 2 != 0:
	#     	leg.displace_tip(0,  60, 0)
	#     else:
	#     	leg.displace_tip(0,  0, 0)

	# time.sleep(speed)

	# for leg in spido.legs:
	#     if leg.number % 2 != 0:
	#     	leg.displace_tip(0,  0, 60)
	#     else:
	#     	leg.displace_tip(0,  0, 0)
	# time.sleep(speed)

	# for leg in spido.legs:
	#     leg.position  = 150, 150, 150
	#     spido.spread(30)
	# time.sleep(speed)

	# time.sleep(5.0)
	# for leg in spido.legs:
	#     if leg.number % 2 == 0:
	#     	leg.displace_tip(0,  0, -10)
	#     else:
	#     	leg.displace_tip(0,  50, 0)

time.sleep(1.0)