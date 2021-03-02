from Chassis import Chassis
import socket
from time import sleep
from DriveDetect import DriveDetect

RPWMF = 22  # PWM
RPWMB = 29

LPWMF = 31  # PWM
LPWMB = 36

DIR = 38
STEP = 35
SWITCH = 13

GRIPPER = 1
ELBOW = 0
BUCKET = 2

resolution = "640x360"

chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB, STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET)
driveDetect = DriveDetect(chassis, resolution)

current_state = b'drive'
trash_detected = False
trash_count = 0
last_turn = ' '

TCP_IP = '192.168.4.2'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)

recieved = ""

counter = 0
finished_clean = False

while not finished_clean or trash_count < 4:

    if trash_count >= 4:
        current_state = b'stop'

    # Constantly updating current yaw angle
    euler_angles = chassis.IMU.euler_from_quaternion()

    data = conn.recv(BUFFER_SIZE)

    if data != b'middle':
        current_state = data

    if current_state == b'drive':
        driveDetect.cleanLitter()
    elif current_state == b'turnleft':
        chassis.swing_turn_IMU(chassis, euler_angles, -180, 5, 50)
        if abs(-10 - euler_angles) < 0.5:
            current_state = b'drive'
    elif current_state == b'turnright':
        chassis.swing_turn_IMU(chassis, euler_angles, 180, 5, 50)
        if abs(10 - euler_angles) < 0.5:
            current_state = b'drive'
    elif current_state == b'stop':
        chassis.drive(0, 0)
        break

    conn.send(data)  # echo

conn.close()