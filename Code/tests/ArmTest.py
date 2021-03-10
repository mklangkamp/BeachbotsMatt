import sys
from small_bot from Chassis import Chassis
from Arm import Arm
from ServoController import ServoController
#from time import sleep
#import time


DIR = 38
STEP = 35
SWITCH = 13

GRIPPER = 1
ELBOW = 0
BUCKET = 2

DOWN_POSE_ELBOW = 5300
UP_POSE_ELBOW = 8000

#usleep = lambda x: time.sleep(x/1000000.0)
arm = Arm(STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET)

RPWMF = 22  # PWM
RPWMB = 29

LPWMF = 31  # PWM
LPWMB = 36
chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB)

arm.pickup(0)
Chassis.driveStraightIMU(chassis, 50, 1000)
arm.pickup(1)
    #print(arm.switch_press())
#while True:
#    arm.switch_press()
#    print(arm.switch_press())
#arm.move_shoulder_angle(30)
# servo.elbow(DOWN_POSE_ELBOW)
#servo.gripper(False)
#arm.calibrate()
#arm.move_shoulder_angle(20)
#Chassis.driveStraightIMU(chassis, 50, 1000)
#arm.move_shoulder_angle(-10)

    