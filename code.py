# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Servo standard servo example"""

from time import sleep

import board
import pwmio
from adafruit_motor import servo

import usb_cdc

import random

# create a PWMOut object on Pin A1.
pwm1 = pwmio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=50)
# create a PWMOut object on Pin A2.
pwm2 = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo1 = servo.Servo(pwm1)
my_servo2 = servo.Servo(pwm2)

class Channel:
    channels = dict()
    
    def __init__(self, prefix, func, **kwargs):
        self.channels[prefix] = self
        self.prefix = prefix
        
        self.func = func
        self.kwargs = kwargs
        
    
    def action(self, data):
        return self.func(data, self.kwargs)
    
    
def recieve(data):
    data = data[:-1]
    i = data[0:1]
    data = data[1:]

    return i, data
        
        
        
def turn_servo(data, kwargs):
    angle = int(data)
    if angle > 0 and angle <= 180:
        kwargs['my_servo'].angle = angle
    return angle
  
def random_number(data, kwargs):
    angle = int(data)
    return random.random()
        
channel1 = Channel(b'\x00', turn_servo, my_servo=my_servo1)
channel2 = Channel(b'\x01', turn_servo, my_servo=my_servo2)
channel3 = Channel(b'\x02', random_number)

while True:
    line = usb_cdc.data.readline()
    i, data = recieve(line)

    channel = Channel.channels.get(i)
    #print(i, data)

    result = channel.action(data)
    
    y = channel.prefix + bytes(str(result), 'utf-8') + b'\n'
    #print(y)
    usb_cdc.data.write(y)
"""
i = 0
while True:
    my_servo.angle = 0
    sleep(1.5)
    my_servo.angle = 180
    sleep(1.5)
    print(i)
    i += 1
"""


