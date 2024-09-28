# echo-server.py

import socket
import serial



HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

serial = serial.Serial('/dev/ttyACM1', baudrate=115200, timeout=0.01)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        connection, addr = s.accept()
        with connection:
            print(f"Connected by {addr}")
            while True:
                data = connection.recv(1024)
                serial.write(data)
                print(data)
                if not data:
                    break
                data = serial.read_until()
                connection.sendall(data)

