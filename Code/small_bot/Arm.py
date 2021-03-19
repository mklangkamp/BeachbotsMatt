# title           :Arm.py
# description     :Class for the 2 DOF arm
# author          :Dennis Chavez Romero, Spencer Gregg
# date            :2021-02-05
# version         :0.1
# notes           :
# python_version  :3.7
# ==============================================================================
import RPi.GPIO as GPIO
import time
from time import sleep
from ServoController import ServoController
import sys
sys.path.insert(0, '/home/pi/beachbots2020/Code/support')
import Constants

class Arm:

    def __init__(self, STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET):
        """
        Class constructor
        """

        # Pins for step pulse and direction
        self.STEP = STEP
        self.DIR = DIR

        # Pin for limit switch
        self.SWITCH = SWITCH

        # Instance of servo controller
        self.servo = ServoController(GRIPPER, ELBOW, BUCKET)

        # Set pin numbering system
        GPIO.setmode(GPIO.BOARD)

        # Disable warnings
        GPIO.setwarnings(False)

        # Setup pins as OUT for output and IN for input
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.SWITCH, GPIO.IN)

        # Lambda function for sleeps with microseconds
        self.usleep = lambda x: time.sleep(x / 1000000.0)

        # Variable for angle of stepper motor at any point in time
        self.shoulder_current = 0.0

        # Calibrate arm joints upon instantiation
        self.calibrate()

    def move_shoulder_angle(self, angle):
        """
        Moves the stepper motor to given angle (in degrees)
        :param angle     [int]  The angle to move the stepper motor to (in degrees).
        """

        # Calculate the target angle to go from the current angle
        target = angle - self.shoulder_current

        # Calculate the number of steps to achieve the calculated target
        steps = abs(int(target // Constants.STEP_ANGLE))

        num_steps = 0

        # Determine direction that the motor needs to go to based on target sign
        if target < 0:
            # If needs to go to a negative angle
            # Then set DIR(ection) to LOW
            GPIO.output(self.DIR, GPIO.LOW)
        else:
            # If needs to go to a positive angle
            # Then set DIR(ection) to HIGH
            GPIO.output(self.DIR, GPIO.HIGH)

        # Keep moving arm while the number of steps needed to get to target has not been achieved
        while num_steps < steps:
            GPIO.output(self.STEP, GPIO.HIGH)
            self.usleep(500)
            GPIO.output(self.STEP, GPIO.LOW)
            self.usleep(500)
            num_steps += 1

        # Update current shoulder angle
        self.shoulder_current += target

    def calibrate(self):
        """
        Zeros stepper motor and sets servo values to default
        """

        # Set bucket to default position
        self.servo.bucket(False)

        # Set elbow servo to its default pose
        self.servo.elbow(Constants.UP_POSE_ELBOW)

        # Set gripper to closed position
        self.servo.gripper(False)

        # Set the DIR pin to low
        GPIO.output(self.DIR, GPIO.LOW)

        # Keep driving the stepper motor down while it has not hit the limit switch
        while not GPIO.input(self.SWITCH):
            GPIO.output(self.STEP, GPIO.HIGH)
            self.usleep(500)
            GPIO.output(self.STEP, GPIO.LOW)
            self.usleep(500)

        # Once the limit switch has been toggled, we can zero the current shoulder angle
        self.shoulder_current = 0

        # Move the arm to an angle of 30 to be parallel with the ground
        self.move_shoulder_angle(30)

    def pickup(self):
        """
        Executes the motions needed to pickup a piece of trash.
        """

        # Elevate the shoulder
        self.move_shoulder_angle(100)
        sleep(2)

        # Open gripper
        self.servo.gripper(True)
        sleep(4)

        # Set the elbow to its pickup pose
        self.servo.elbow(Constants.DOWN_POSE_ELBOW)
        sleep(3)

        # Lower shoulder
        self.move_shoulder_angle(45)

        # Close gripper
        self.servo.gripper(False)
        sleep(3)

        # Elevate elbow towards bucket
        self.servo.elbow(Constants.UP_POSE_ELBOW)

        # Elevate shoulder
        self.move_shoulder_angle(115)
        sleep(2)

        # Open gripper
        self.servo.gripper(True)
        sleep(3)

        # Bring shoulder back to its original position
        self.move_shoulder_angle(30)

        # Close gripper
        self.servo.gripper(False)
