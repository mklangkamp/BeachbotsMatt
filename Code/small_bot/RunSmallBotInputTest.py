# title           :RunSmallBot.py
# description     :Cleans trash seen and drives predetermined path received from the BaseBot
# author          :Dennis Chavez Romero, Spencer Gregg
# date            :2021-03-07
# version         :0.1
# notes           :
# python_version  :3.7
# ==============================================================================
from Chassis import Chassis
from SmallBotCom import TCP_COMM
from DriveDetect import DriveDetect
from time import sleep
import sys
sys.path.insert(0, '/home/pi/beachbots2020/Code/support')
import Constants

# Instance of chassis
chassis = Chassis(Constants.RPWMF, Constants.RPWMB, Constants.LPWMF, Constants.LPWMB, Constants.STEP, Constants.DIR,
                  Constants.SWITCH, Constants.GRIPPER, Constants.ELBOW, Constants.BUCKET)

# Instance of DriveDetect class
driveDetect = DriveDetect(chassis, Constants.RESOLUTION, Constants.VIEW_ANGLE)

# Instance of basebot
base_bot = TCP_COMM(Constants.TCP_IP, Constants.TCP_PORT, Constants.BUFFER_SIZE)

# Starting variables before cleanup
current_state = b'none'

finished_clean = False

# Perform cleanup while the smallbot has not finished the path or while it is not at full carrying capacity
while not finished_clean and not driveDetect.is_full_capacity():

    # Constantly receive data from the basebot
    current_state = base_bot.get_data()

    # Drive and scan for litter
    if current_state == b'drive':
        driveDetect.clean_litter()

    # If the smallbot needs to turn
    elif current_state == b'turnright' or current_state == b'turnleft':

        # Check the direction it needs to turn to
        if current_state == b'turnright':
            is_done_turning = chassis.point_turn_basebot(90, Constants.MOTOR_SPEED)
        elif current_state == b'turnleft':
            is_done_turning = chassis.point_turn_basebot(-90, Constants.MOTOR_SPEED)

        # Once it is done turning
        if is_done_turning:
            # Update with basebot latest data
            base_bot.get_data()

            # Send confirmation that turn has been completed
            base_bot.send_turning_confirmation(b'done_turning')

            # Reset IMU heading back to 0 for future turns
            chassis.reset_heading()

    # Drive straight with IMU with negative wheel efforts when driving backwards
    elif current_state == b'drivebackwards':
        chassis.drive_straight_IMU(-Constants.MOTOR_SPEED, 0)

    # If ordered to dump bucket
    elif current_state == b'dump':
        # Actuate bucket
        chassis.arm.servo.bucket(True)

        # Wait for 3 seconds for trash to empty
        sleep(3)

        # Set bucket back to default position
        chassis.arm.servo.bucket(False)

        # Indicate that the cleaning has been completed
        finished_clean = True

    elif current_state == b'stop' or current_state == b'none':
        chassis.drive(0, 0)

base_bot.close_conn()
exit()
