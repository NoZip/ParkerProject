import math
from math import cos, sin, acos, atan

r0 = 52.0
d0 = 15.0
r1 = 64.0
theta1 = 0.366
r2 = 93.0
theta2 = -0.511 + math.pi/2
# print(math.degrees(theta1))
# print(math.degrees(theta2))

def forward_kin(t0, t1, t2):
    return forward_kin_rads(math.radians(t0),
                            math.radians(t1),
                            math.radians(t2))

def forward_kin_rads(t0, t1, t2):
    x =(r0*cos(t0)
      + r1*cos(t0)*cos(t1 + theta1)
      + r2*cos(t0)*cos(t1 + t2 + theta1 + theta2)
       )

    y =(r0*sin(t0)
      + r1*sin(t0)*cos(t1 + theta1)
      + r2*sin(t0)*cos(t1 + t2 + theta1 + theta2)
       )

    z =(d0
      + r1*sin(t1 + theta1)
      + r2*sin(t1 + t2 + theta1 + theta2)
       )

    return (x, y, z)


def alpha(x, y, z):
    try:
      return math.degrees(atan(y/x))
    except ZeroDivisionError:
      return 0.0

def acos_safe(a):
    return math.acos(max(-1.0, min(1.0, a)))

def gamma(x, y, z):
    w_xy = x*x + y*y
    w = w_xy + z*z
    return math.degrees(acos_safe((w - r1*r1 - r2*r2)/(2*r1*r2))) - 60.72185666881492

def beta_off(x, y, z):
    w_xy = x*x + y*y
    w = w_xy + z*z
    return math.degrees(acos_safe((r2*r2 - r1*r1 - w)/(-2*r1*math.sqrt(w)))) - 36.5363892715

def beta(x, y, z, a):
    factor = 1 if x >= 0 else -1
    w_xy = math.sqrt(x*x + y*y)
    try:
        if x < 0:
            return math.degrees(atan(factor*z/w_xy)) - 57.50664457329989 + 180
        return math.degrees(atan(factor*z/w_xy)) - 57.50664457329989
    except ZeroDivisionError:
      return 0.0

def inverse_kin(x, y, z):
    a = math.radians(alpha(x, y, z))
    x2, y2, z2 = x-r0*cos(a), y-r0*sin(a), z - d0
    return alpha(x, y, z), beta(x2,y2,z2, a) - beta_off(x2, y2, z2), gamma(x2, y2, z2)

