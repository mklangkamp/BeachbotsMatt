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

itteration = 0

#Driving test starts here... ...
while(itteration <= 0):

    servo.elbow(UP_POSE_ELBOW)
    sleep(1)

    Chassis.drive(chassis, 50)
    print("Forward")
    sleep(1)
    Chassis.estop(chassis)
    print("Stop")
    sleep(1)
    Chassis.turn(chassis, 100, 50)
    print("Right")
    sleep(1)
    Chassis.estop(chassis)
    print("Stop")
    sleep(1)
    # Chassis.turn(chassis, 100, -50)
    # print("Left")
    # sleep(1)
    print(" ")
    print(" ")
    print(" ")

    Chassis.estop(chassis)

    servo.elbow(DOWN_POSE_ELBOW)
    sleep(3)

    servo.gripper(True)
    sleep(2)

    Chassis.drive(chassis, 50)
    servo.gripper(False)
    sleep(1)
    Chassis.estop(chassis)


    #sleep(2)

    servo.elbow(UP_POSE_ELBOW)
    arm.move_shoulder(1, SHOULDER_UP_DOWN_TIME)


    servo.gripper(True)
    sleep(2)

    arm.move_shoulder(-1, SHOULDER_UP_DOWN_TIME)
    sleep(1)

    servo.gripper(False)

    Chassis.drive(chassis, -50)
    sleep(1)
    Chassis.estop(chassis)
    sleep(1)
    Chassis.turn(chassis, 100, -50)
    sleep(1)
    Chassis.estop(chassis)
    #servo.elbow(DOWN_POSE_ELBOW)
    servo.bucket(True)

    sleep(1)

    servo.bucket(False)

    itteration = itteration + 1






# if state == False:
#
#
#     servo.gripper(True)
#
#     servo.elbow(DOWN_POSE_ELBOW)
#     servo.bucket(False)
#
#
# elif state == True:
#
#     servo.elbow(UP_POSE_ELBOW)
#     arm.move_shoulder(1, SHOULDER_UP_DOWN_TIME)
#
#     servo.gripper(True)
#     sleep(2)
#
#     arm.move_shoulder(-1, SHOULDER_UP_DOWN_TIME)
#     sleep(1)
#
#     servo.elbow(DOWN_POSE_ELBOW)
#     servo.bucket(True)
#
#     sleep(1)
#
#     servo.bucket(False)
#     servo.gripper(False)

