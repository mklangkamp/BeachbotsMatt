from Chassis import Chassis
from AdafruitIMU import AdafruitIMU
from time import sleep
import socket

RPWMF = 22  # PWM
RPWMB = 29

LPWMF = 31  # PWM
LPWMB = 36
chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB)
IMU = AdafruitIMU()
itteration = 0

TCP_IP = '192.168.4.2'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#Driving test starts here... ...
#while(itteration <= 0):
#Chassis.driveStraightIMU(chassis, 50, 1000)



    
#Chassis.point_turn_IMU(chassis, euler_angles, 10, 5, 25)
#if abs(10-euler_angles) < 0.5:
#    Chassis.drive(0, 0)
#     break
#recieved = ""
current_state = " "
conn, addr = s.accept()
print ('Connection address:', addr)
'''
counter = 0
while True:
    euler_angles = IMU.euler_from_quaternion()
    #print(euler_angles)
    print("times ran: ", counter)
    data = conn.recv(BUFFER_SIZE)
    conn.send(data)
    counter = counter + 1
'''
while 1:
    euler_angles = IMU.euler_from_quaternion()
    print(euler_angles)
    data = conn.recv(BUFFER_SIZE)
    #if not data:
    #    print("gooddaymite")
    #    break
    #if len(data) != 0:
    #    recieved = data
    
    if data != b'middle':
        current_state = data
    #print("hi")
    print("received data:", current_state)
    if current_state == b'turnleft':
        Chassis.swing_turn_IMU(chassis, euler_angles, -10, -5, 50)
        print(euler_angles)
        if abs(-10-euler_angles) < 0.5:
            Chassis.drive(0, 0)
            break
    
    elif current_state == b'turnright':
        Chassis.swing_turn_IMU(chassis, euler_angles, 10, 5, 50)
        #print(euler_angles)
        if abs(10-euler_angles) < 0.5:
            Chassis.drive(0, 0)
            break
    elif current_state == b'stop':
        Chassis.drive(0, 0)
        break
    conn.send(data) #was data # echo
conn.close()
Chassis.drive(0, 0)





