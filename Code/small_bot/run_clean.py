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

TCP_IP = '192.168.137.210'#'192.168.4.2'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB, STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET)
driveDetect = DriveDetect(chassis, resolution, camera_view_angle)
base_bot = TCP_COMM(TCP_IP, TCP_PORT, BUFFER_SIZE)

current_state = b'none'
trash_detected = False
trash_count = 0

counter = 0
finished_clean = False

'''
while True:
    base_bot.get_data()

'''
'''
current_heading = chassis.IMU.euler_from_quaternion()

print("first heading: :", current_heading)

while chassis.IMU.euler_from_quaternion() < 10:
    
    current_loop_heading = chassis.IMU.euler_from_quaternion()
    #print("waiting to turn...")
    if current_loop_heading > 10:
        print("current heading: :", current_loop_heading)
        chassis.reset_heading()
        break

current_heading = chassis.IMU.euler_from_quaternion()

print("updated heading: :", current_heading)
print("current heading: :", chassis.IMU.euler_from_quaternion())
'''

while not finished_clean or not driveDetect.is_full_capacity():

    # Constantly updating current yaw angle
    # euler_angles = chassis.IMU.euler_from_quaternion()

    # if base_bot.get_data() != b'middle':
    #    current_state = base_bot.get_data()
    
    
    if current_state == b'drive':
        #pass
        
        driveDetect.cleanLitter()
    elif current_state == b'turnright':
        isDoneTurning = chassis.point_turn_basebot(90, 20)
        
        if isDoneTurning:
            base_bot.get_data()
            base_bot.send_turning_confirmation(b'done_turning')
            chassis.reset_heading()
    elif current_state == b'none':
        chassis.drive(0, 0)
    
    current_state = base_bot.get_data()
    #base_bot.get_data()

base_bot.close_conn()

