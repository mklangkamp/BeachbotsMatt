from Chassis import Chassis
from Arm import Arm
from ServoController import ServoController
from time import sleep

state = True

RPWMF = 22  # PWM
RPWMB = 29

LPWMF = 31  # PWM
LPWMB = 36

#for stepper
DIR = 38
STEP = 35

GRIPPER = 1
ELBOW = 0
BUCKET = 2

#Magic numbers
DOWN_POSE_ELBOW = 5300
UP_POSE_ELBOW = 8000
SHOULDER_UP_DOWN_TIME = 2400

chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB)
arm = Arm(STEP, DIR)
servo = ServoController(GRIPPER, ELBOW, BUCKET)


if state == False:


    servo.gripper(True)

    servo.elbow(DOWN_POSE_ELBOW)
    servo.bucket(False)


elif state == True:

    servo.elbow(UP_POSE_ELBOW)
    arm.move_shoulder(1, SHOULDER_UP_DOWN_TIME)

    servo.gripper(True)
    sleep(2)

    arm.move_shoulder(-1, SHOULDER_UP_DOWN_TIME)
    sleep(1)

    servo.elbow(DOWN_POSE_ELBOW)
    servo.bucket(True)

    sleep(1)

    servo.bucket(False)
    servo.gripper(False)

