import serial

from time import sleep

serial = serial.Serial('/dev/ttyACM1', baudrate=115200, timeout=0.01)


while True:
    serial.write(b'\n')
    x = serial.readlines()
    if x != []:
        print("temperature: {} relative_humidity: {}".format(x[0], x[1]))
