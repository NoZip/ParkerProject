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

#150.0, 60.0,  60.0,
# 150.0, 240.0, 240.0
# spido.legs[2].position = 150,240,240
# spido.legs[0].position = 150,60,60
spido.spread(30)

for leg in spido.legs:
    raw_input()
    leg.displace_tip(0,  60, -20)
    time.sleep(1.0)
    leg.displace_tip(0, -60,  20)

time.sleep(1.0)