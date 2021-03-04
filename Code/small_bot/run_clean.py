from Chassis import Chassis
from small_comm import TCP_COMM
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
camera_view_angle = 60

TCP_IP = '192.168.4.2'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB, STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET)
driveDetect = DriveDetect(chassis, resolution, camera_view_angle)
base_bot = TCP_COMM(TCP_IP, TCP_PORT, BUFFER_SIZE)

current_state = b'drive'
trash_detected = False
trash_count = 0

counter = 0
finished_clean = False

while not finished_clean or trash_count < 4:

    if trash_count >= 4:
        current_state = b'stop'

    # Constantly updating current yaw angle
    euler_angles = chassis.IMU.euler_from_quaternion()

    if base_bot.get_data() != b'middle':
        current_state = base_bot.get_data()

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

base_bot.close_conn()
