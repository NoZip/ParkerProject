import pydyn

ctrl = pydyn.dynamixel.create_controller(motor_range=[0, 20], verbose = True)
for m in ctrl.motors:
    m.compliant = True
ctrl.wait(2)