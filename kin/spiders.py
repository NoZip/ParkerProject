import kin

# each motor is given the positional id ab, with a the leg number (0 being the one closest to the power plug),
# and b among 0, 1, 2 in proximo distal order.

# that define the global order or motors, as the numerical one.
pos_name = set(['position', 'goal_position', 'cw_angle_limit', 'ccw_angle_limit', 'present_position'])

n = 4
#                0,  1,  2,   3,  4,  5,   6,  7,  8,   9, 10, 11,  12, 13, 14,  15, 16, 17
spiders_ids = (( 8,  7,  9,   15, 11, 12,  10,  4, 16,  13, 2, 18,    6,  5,  1,  17,  3, 14),
               (14, 16, 18,    8, 10, 12,   2,  4,  6,   1, 3,  5,    7,  9, 11,  13, 15, 17),
               ( 1,  3,  5,    7,  9, 11,  13, 15, 17,  14, 16, 18,   8, 10, 12,   2,  4,  6),
               ( 1,  3,  5,   13, 15, 17,   7,  9, 11,  14, 16, 18,   8, 10, 12,   2,  4,  6),
               ( 7,  9, 11,    1,  3,  5,  13, 15, 17,  14, 16, 18,   8, 10, 12,   2,  4,  6),
              )

# This is orientations *after* reodering !
spiders_ori = (( 1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1),
               ( 1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1),
               ( 1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1),
               ( 1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1),
               ( 1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1,   1, -1,  1),
              )

spiders_off = ((150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  186.0, 150.0, 150.0,  150.0, 150.0, 150.0),
               (150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0),
               (150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0),
               (150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0),
               (150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0,  150.0, 150.0, 150.0),
              )

leg_axis = (( 0,  1), ( 0,  1), ( 1,  0), ( 1,  0), ( 0,  1), ( 0,  1))
leg_dir  = (( 1,  1), ( 1,  1), (-1, -1), (-1, -1), (-1, -1), ( -1,  -1))


class MotorInterface(object):

    def __init__(self, motor, orientation = 1, offset = 150.0):
        assert orientation == 1 or orientation == -1
        object.__setattr__(self, 'motor',       motor)
        object.__setattr__(self, 'orientation', orientation)
        object.__setattr__(self, 'offset',      offset)

    def __setattr__(self, name, value):
        if name in pos_name:
            return self.motor.__setattr__(name, self._pos2real(value))
        return self.motor.__setattr__(name, value)

    def __getattr__(self, name):
        if name in pos_name:
            return self._real2pos(self.motor.__getattribute__(name))
        return self.motor.__getattribute__(name)

    def _pos2real(self, pos):
        return (pos - 150.0) * self.orientation + self.offset

    def _real2pos(self, pos):
        return (pos - self.offset) * self.orientation + 150.0


class SpiderInterface(object):

    def __init__(self, ctrl, n = n):
        assert len(ctrl.motors) == 18
        self.n    = n
        self.ctrl = ctrl

        self.motors = []
        for k, m in enumerate(ctrl.motors):
            m = self.ctrl.motors[spiders_ids[n][k] - 1]
            self.motors.append(MotorInterface(m, spiders_ori[n][k], spiders_off[n][k]))
        self._create_legs()

    def _create_legs(self):
        assert len(self.motors) == 18
        self.legs = []
        for i in range(6):
            self.legs.append(Leg(i, [self.motors[3*i], self.motors[3*i+1], self.motors[3*i+2]]))

    def spread(self, angle):
        assert angle >= 0
        proximal_pose = (150-angle, 150, 150+angle, 150-angle, 150, 150+angle)
        for p_i, leg in zip(proximal_pose, self.legs):
            leg.proximo.position = p_i

class Leg(object):
    """Hexapod leg.
    Is made of three motors (interfaces) given in proximo-distal order.
    """

    def __init__(self, number, motors):
        assert len(motors) == 3
        object.__setattr__(self, 'number', number)
        object.__setattr__(self, 'motors', motors)
        object.__setattr__(self, 'proximo', motors[0])
        object.__setattr__(self, 'middle',  motors[1])
        object.__setattr__(self, 'distal',  motors[2])

    def __setattr__(self, name, value):
        if hasattr(value, '__iter__'):
            if len(value) == 3:
                for v_i, m_i in zip(value, self.motors):
                    if v_i is not None:
                        setattr(m_i, name, v_i)
            else:
                raise ValueError, 'Too many or to little value to set: expected 3, got {}.'.format(len(value))
        else:
            if value is not None:
                for motor in self.motors:
                    setattr(motor, name, value)

    def __getattr__(self, name):
        return tuple(getattr(motor, name) for motor in self.motors)

    def _leg2global(self, pos):
        x = leg_dir[self.number][0]*pos[leg_axis[self.number][0]]
        y = leg_dir[self.number][1]*pos[leg_axis[self.number][1]]
        z = pos[2]
        return x, y, z

    def _global2leg(self, pos):
        x = leg_dir[self.number][0]*pos[leg_axis[self.number][0]]
        y = leg_dir[self.number][1]*pos[leg_axis[self.number][1]]
        z = pos[2]
        return x, y, z

    @property
    def tip(self):
        alpha = self.proximo.position - 150.0
        beta  = - (self.middle.position - 150.0)
        gamma = - (self.distal.position - 150.0)
        return self._leg2global(kin.forward_kin(alpha, beta, gamma))

    def displace_tip(self, dx, dy, dz):
        x, y, z = self.tip
        alpha = self.proximo.position - 150.0
        beta  = - (self.middle.position - 150.0)
        gamma = - (self.distal.position - 150.0)

        xdx, ydy, zdz = self._global2leg((x+dx, y+dy, z+dz))
        alpha, beta, gamma = kin.inverse_kin(xdx, ydy, zdz)
        self.proximo.position = alpha + 150.0
        self.middle.position  = 150.0 - beta
        self.distal.position  = 150.0 - gamma


