# title           :ServoController.py
# description     :Controller for onboard servos connected to the Maestro Controller
# author          :Dennis Chavez Romero, Spencer Gregg, Yossef Naim
# date            :2020-12-05
# version         :0.1
# notes           :
# python_version  :3.7
# ==============================================================================
import Maestro
import sys
sys.path.insert(0, '/home/pi/beachbots2020/Code/support')
import Constants


class ServoController:
    def __init__(self, GRIPPER, ELBOW, BUCKET):
        """
        Class constructor
        """

        # Instance of Maestro controller
        self.servo = Maestro.Controller()

        # Controller pins
        self.gripper_pin = GRIPPER
        self.elbow_pin = ELBOW
        self.bucket_pin = BUCKET

        self.delay = 0.001

    def gripper(self, val, accel=5, speed=15):
        """
        :param val       [bool] True opens the gripper, False closes the gripper.
        :param accel     [int]  Acceleration of servo.
        :param speed     [int]  Speed of servo movement.
        """

        # Set gripper acceleration
        self.servo.setAccel(self.gripper_pin, accel)

        # Set gripper speed
        self.servo.setSpeed(self.gripper_pin, speed)

        if val:
            self.servo.setTarget(self.gripper_pin, Constants.GRIPPER_OPEN_VAL)
        else:
            self.servo.setTarget(self.gripper_pin, Constants.GRIPPER_CLOSED_VAL)

    def get_gripper_pos(self):
        """
        Getter for gripper position
        :return        [int] Position of the gripper
        """

        # Get the current position of gripper servo
        return self.servo.getPosition(self.gripper_pin)

    def bucket(self, val, accel=15, speed=45):
        """
        :param val       [bool] True opens the bucket, False closes the bucket.
        :param accel     [int]  Acceleration of servo.
        :param speed     [int]  Speed of servo movement.
        """

        # Set bucket acceleration
        self.servo.setAccel(self.bucket_pin, accel)

        # Set bucket speed
        self.servo.setSpeed(self.bucket_pin, speed)

        if val:
            self.servo.setTarget(self.bucket_pin, Constants.BUCKET_DISPOSE_VAL)
        else:
            self.servo.setTarget(self.bucket_pin, Constants.BUCKET_DEFAULT_VAL)

    def get_bucket_pos(self):
        """
        Getter for bucket position
        :return        [int] Position of the bucket
        """

        # Get the current position of bucket servo
        return self.servo.getPosition(self.bucket_pin)

    def elbow(self, val, accel=5, speed=15):
        """
        :param val       [int]  Position for the elbow to go to.
        :param accel     [int]  Acceleration of servo.
        :param speed     [int]  Speed of servo movement.
        """

        # Set elbow acceleration
        self.servo.setAccel(self.elbow_pin, accel)

        # Set servo speed
        self.servo.setSpeed(self.elbow_pin, speed)

        # Set elbow position value
        self.servo.setTarget(self.elbow_pin, val)

    def get_elbow_pos(self):
        """
        Getter for elbow position
        :return        [int] Position of the elbow
        """

        # Get the current position of elbow servo
        return self.servo.getPosition(self.elbow_pin)
