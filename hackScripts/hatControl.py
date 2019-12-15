#!/usr/bin/python3

from adafruit_servokit import ServoKit

# init 16 channels hat
kit = ServoKit(channels=16)

# x at channel 0
# y at  channel 1
x = kit.servo[0]
y = kit.servo[1]

# 500 microseconds  = 0 deg
# 1500 microseconds = 90 deg
# 2500 microseconds = 180 deg
x.set_pulse_width_range(500,2500)
y.set_pulse_width_range(500,2500)

# init at 90 deg(flat)
x.angle = 90
y.angle = 90

def xChange(angle):
    x.angle = calculate(angle)

def yChange(angle):
    y.angle = calculate(angle)


def calculate(angle):
    # enlarge the input angle
    angle = angle*2 + 90
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    return round(angle, 2)
