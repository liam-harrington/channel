from inputs import get_gamepad

from time import sleep

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

class Channel:
    SUFFIX = '\n'

    def __init__(self, s, prefix):
        self.s = s
        self.prefix = prefix
        
    def get_bytes(self, data):
        return self.prefix + (str(data) + '\n').encode()
        
    def send(self, data):
        #serial.write(self.get_bytes(y))
        self.s.sendall(self.get_bytes(y))
        data = self.s.recv(1024)
        print(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    channel1 = Channel(s, b'\x00')
    channel2 = Channel(s, b'\x01')
    channel3 = Channel(s, b'\x02')
    while True:
        events = get_gamepad()
        for event in events:
            #print(event.ev_type, event.code, event.state)
            if event.code == 'ABS_Z':
                #print(event.ev_type, event.code, event.state)
                x = event.state / 255
                y = int(x * 180)
                
                
                channel1.send(y)
                #print(y)
    
            elif event.code == 'ABS_RZ':
                #print(event.ev_type, event.code, event.state)
                x = event.state / 255
                y = int(x * 180)
                
                
                channel2.send(y)
                #print(y)
            elif event.code == 'BTN_TRIGGER':
                #print(event.ev_type, event.code, event.state)
                x = event.state / 1
                y = int(x * 180)
                
                
                channel3.send(y)
                #print(y)

        """
        data = serial.read_until()   
        if data != b'':
            data = data[:-1]
            i = data[0:1]
            data = data[1:]
            print(i, data)
        """
