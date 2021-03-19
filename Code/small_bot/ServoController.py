import Maestro
import sys
sys.path.insert(0, '/home/pi/beachbots2020/Code/support')

import Constants


class ServoController:
    def __init__(self, GRIPPER, ELBOW, BUCKET):

        self.servo = Maestro.Controller()

        # Pins
        self.gripper_pin = GRIPPER
        self.elbow_pin = ELBOW
        self.bucket_pin = BUCKET

        self.delay = 0.001

    def gripper(self, val, accel=5, speed=15):
        """
        :param val: True opens the gripper, False closes the gripper
        :param accel: acceleration of servo
        :param speed: speed of servo movement
        :return: void
        """
        self.servo.setAccel(self.gripper_pin, accel)  # set gripper acceleration
        self.servo.setSpeed(self.gripper_pin, speed)  # set gripper speed

        if val:
            self.servo.setTarget(self.gripper_pin, Constants.GRIPPER_OPEN_VAL)
        else:
            self.servo.setTarget(self.gripper_pin, Constants.GRIPPER_CLOSED_VAL)

    def get_gripper_pos(self):
        """
        Getter for gripper position
        :return: Position of the gripper
        """
        return self.servo.getPosition(self.gripper_pin)  # get the current position of gripper servo

    def bucket(self, val, accel=15, speed=45):
        """
        :param val: True opens the gripper, False closes the gripper
        :param accel: acceleration of servo
        :param speed: speed of servo movement
        :return: void
        """
        self.servo.setAccel(self.bucket_pin, accel)  # set gripper acceleration
        self.servo.setSpeed(self.bucket_pin, speed)  # set gripper speed

        if val:
            self.servo.setTarget(self.bucket_pin, Constants.BUCKET_DISPOSE_VAL)  # set gripper position
        else:
            self.servo.setTarget(self.bucket_pin, Constants.BUCKET_DEFAULT_VAL)  # set gripper position

    def get_bucket_pos(self):
        """
        Getter for gripper position
        :return: Position of the gripper
        """
        return self.servo.getPosition(self.bucket_pin)  # get the current position of gr

    def elbow(self, val, accel=5, speed=15):
        """
        :param val: True opens the gripper, False closes the gripper
        :param accel: acceleration of servo
        :param speed: speed of servo movement
        :return: void
        """
        self.servo.setAccel(self.elbow_pin, accel)  # set gripper acceleration
        self.servo.setSpeed(self.elbow_pin, speed)  # set gripper speed
        self.servo.setTarget(self.elbow_pin, val)  # set gripper position

    def get_elbow_pos(self):
        """
        Getter for gripper position
        :return: Position of the elbow
        """
        return self.servo.getPosition(self.elbow_pin)  # get the current position of elbow servo
