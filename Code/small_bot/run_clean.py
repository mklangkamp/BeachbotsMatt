from Chassis import Chassis
from small_comm import TCP_COMM
from DriveDetect import DriveDetect
from time import sleep
import sys
sys.path.insert(0, '/home/pi/beachbots2020/Code/support')

import Constants


chassis = Chassis(Constants.RPWMF, Constants.RPWMB, Constants.LPWMF, Constants.LPWMB, Constants.STEP, Constants.DIR, Constants.SWITCH, Constants.GRIPPER, Constants.ELBOW, Constants.BUCKET)
driveDetect = DriveDetect(chassis, Constants.RESOLUTION, Constants.VIEW_ANGLE)
base_bot = TCP_COMM(Constants.TCP_IP, Constants.TCP_PORT, Constants.BUFFER_SIZE)

current_state = b'none'
trash_detected = False
trash_count = 0

counter = 0
finished_clean = False

while not finished_clean and not driveDetect.is_full_capacity():

    current_state = base_bot.get_data()
    
    
    if current_state == b'drive':
        driveDetect.cleanLitter()
    elif current_state == b'turnright' or current_state == b'turnleft':

        if current_state == b'turnright':
            isDoneTurning = chassis.point_turn_basebot(90, Constants.MOTOR_SPEED)
        elif current_state == b'turnleft':
            isDoneTurning = chassis.point_turn_basebot(-90, Constants.MOTOR_SPEED)
        
        if isDoneTurning:
            base_bot.get_data()
            base_bot.send_turning_confirmation(b'done_turning')
            chassis.reset_heading()
    elif current_state == b'drivebackwards':
        chassis.driveStraightIMU(-Constants.MOTOR_SPEED, 0)
    elif current_state == b'stop':
        chassis.drive(0, 0)
    elif current_state == b'dump':
        chassis.arm.servo.bucket(True)      
        sleep(3) 
        chassis.arm.servo.bucket(False)
        finished_clean = True
    elif current_state == b'none':
        chassis.drive(0, 0)

base_bot.close_conn()

