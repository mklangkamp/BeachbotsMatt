import RPi.GPIO as GPIO
from Arm import Arm
#from ServoController import ServoController
from time import sleep

DIR = 38
STEP = 35
SWITCH = 13

GRIPPER = 1
ELBOW = 0
BUCKET = 2

DOWN_POSE_ELBOW = 5300
UP_POSE_ELBOW = 8000

arm = Arm(STEP, DIR, SWITCH)
#servo = ServoController(GRIPPER, ELBOW, BUCKET)

while True:
    
    pressed = arm.switch_press()
    if pressed:
        print("button pressed")
    #print(pressed)
    