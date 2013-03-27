import bot
from utils import *
from clock import Clock

def move(bot, (x, y)):
	group1 = list(( bot.legs[1], bot.legs[3], bot.legs[4] ))
	group2 = list(( bot.legs[0], bot.legs[2], bot.legs[5] ))

	time = Clock()

	while time.getTime() < 10 :
		move_z_legs(True, group1)

		if x > 0 :
			move_front(group2)
		elif x < 0 : 
			move_back(group2)

		move_z_legs(False, group1)

		move_z_legs(True, group2)

		if x > 0 :
			move_front(group1)
		elif x < 0 : 
			move_back(group1)

		move_z_legs(False, group2)



def move_front(group):
	pass

def move_back(group):
	pass

def turn(condition):
	if condition :
		turn_left()
	else:		
		turn_right()

def turn_left():
	pass

def turn_right():
	pass

def move_z_legs(up, group):
	z = 0
	
	if up :
		z = 3
	else:
		z = -3

	for leg in group:
		vector = leg.position()
		print(vector)
		leg.move( Vector3D( x = vector.x , y= vector.y, z= (vector.z +z )))