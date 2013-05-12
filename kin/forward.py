import time, sys
import pydyn

import kin
import spiders

ctrl = pydyn.dynamixel.create_controller(motor_range=[0, 20], verbose = True)
spido = spiders.SpiderInterface(ctrl)

posAlhpa = 150
posBeta = 150
posGamma = 150

for leg in spido.legs:
    leg.compliant = False
    leg.position  = posAlhpa, posBeta, posGamma


time.sleep(1.0)

spido.spread(30)

time.sleep(1.0)

speed = 0.45


for motor in ctrl.motors:
		motor.max_torque = 50

time.sleep(1)

while 1:

	####FRAME 1#####
	for leg in spido.legs:
	    if leg.number % 2 == 0:
	    	leg.displace_tip(0,  -80, 80)
	    else:
	    	leg.displace_tip(0,  80, -50)

	time.sleep(speed)

	for leg in spido.legs:
	    leg.position  = posAlhpa, posBeta, posGamma
	    spido.spread(30)


	time.sleep(speed)

	####FRAME 2#####
	for leg in spido.legs:
	    if leg.number % 2 == 0:
	    	leg.displace_tip(0,  80, -50)
	    else:
	    	leg.displace_tip(0,  -80, 80)
	time.sleep(speed)

	for leg in spido.legs:
	    leg.position  = posAlhpa, posBeta, posGamma
	    spido.spread(30)

	time.sleep(speed)


time.sleep(1.0)