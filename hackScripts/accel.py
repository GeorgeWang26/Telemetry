#!/usr/bin/python3
import time

from Adafruit_GPIO.GPIO import *

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# TCP Server Information
#Inital Connection set up
host = '10.8.0.2'
#host = '169.254.181.104'
#host = '10.155.123.77'
#host = '10.152.142.23'
#Static port - Needs to be known
port = 8080

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

#!/usr/bin/python
import smbus
import math
import socket
from statistics import mean

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

#preX = 0
#preY = 0
#weight = 1

xCollect = [0]*10
yCollect = [0]*10
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def createMessage(val):
    return str(round(val,5))

def readAccel():
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)
 
    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0
    
    xRot = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled) / 1
    yRot = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled) / 1

    xCollect.pop(0)
    yCollect.pop(0)
    xCollect.append(xRot)
    yCollect.append(yRot)
	
    messageX = createMessage(mean(xCollect))
    messageY = createMessage(mean(yCollect))
    
    message = messageX + " " + messageY
    
#    print(message)

    s.send(message.encode('UTF-8'))

    #print("({0},{1}) ----> {2}".format(xRot,yRot, round(((float(xRot) + 90) * 512) / 360)))

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect

# Activate to be able to address the module
bus.write_byte_data(address, power_mgmt_1, 0)

print('Press Ctrl-C to quit.')
s = socket.socket()                 #Create socket object
print('ip',host,'port',port)
s.connect((host, port))             #Connect to already running server bind!
print("Connected to computer...")
#variable to keep track of who's turn it is
received = ""
message = "temp"

try:
    while True:
        if message != '':
            readAccel()
            message = ''
        else:
            received = s.recv(4).decode('utf-8')
            message = ' '
except:
#    print("Closing socket...")
    s.close() # You'll get "OSError: [Errno 48] Address already in use" if you don't close right
#    print("Done")
