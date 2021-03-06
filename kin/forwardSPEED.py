import time, sys
import pydyn
from math import cos, sin, radians

import kin
import spiders

def getLegID(leg) :
	if leg == 0 : return 0
	if leg == 5 : return 1
	if leg == 4 : return 2
	if leg == 3 : return 3
	if leg == 2 : return 4
	if leg == 1 : return 5

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
speed = 0.50

for motor in ctrl.motors:
		motor.max_torque = 70
i=0

while i<7:
	r = 80
	####FRAME 1#####
	for leg in spido.legs:
		if leg.number == 1:
			leg.displace_tip(100,0,-100)
		elif leg.number % 2 == 0 :
			leg.displace_tip(10+r*cos(radians((getLegID(leg.number)/6*6.28)+3.14/8)), r*sin(radians((getLegID(leg.number)/6*6.28)+3.14/8)), 80)
		else:
			leg.displace_tip(0,0,-80)

	time.sleep(speed)

	for leg in spido.legs:
		leg.position  = posAlhpa, posBeta, posGamma
		spido.spread(30)
 
	time.sleep(speed)
	i=i+1

speed = 0.35
for motor in ctrl.motors:
		motor.max_torque = 50

time.sleep(1)