import RPi.GPIO as GPIO
import time
from Arm import Arm
from AdafruitIMU import AdafruitIMU

from time import sleep


class Chassis:

    def __init__(self, RPWMF, RPWMB, LPWMF, LPWMB, STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET):
        self.RPWMF = RPWMF
        self.RPWMB = RPWMB
        self.LPWMF = LPWMF
        self.LPWMB = LPWMB
        self.align_threshold = 1.5

        self.IMU = AdafruitIMU()
        self.arm = Arm(STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET)

        GPIO.setwarnings(False)  # disable warnings
        GPIO.setmode(GPIO.BOARD)  # set pin numbering system

        GPIO.setup(self.RPWMF, GPIO.OUT)
        GPIO.setup(self.RPWMB, GPIO.OUT)
        GPIO.setup(self.LPWMF, GPIO.OUT)
        GPIO.setup(self.LPWMB, GPIO.OUT)

        self.pi_rpwmf = GPIO.PWM(self.RPWMF, 1000)  # create PWM instance with frequency
        self.pi_rpwmb = GPIO.PWM(self.RPWMB, 1000)  # create PWM instance with frequency
        self.pi_lpwmf = GPIO.PWM(self.LPWMF, 1000)  # create PWM instance with frequency
        self.pi_lpwmb = GPIO.PWM(self.LPWMB, 1000)  # create PWM instance with frequency

        self.pi_rpwmf.start(0)  # start PWM of required Duty Cycle
        self.pi_rpwmb.start(0)  # start PWM of required Duty Cycle
        self.pi_lpwmf.start(0)  # start PWM of required Duty Cycle
        self.pi_lpwmb.start(0)  # start PWM of required Duty Cycle

    def drive(self, rightSpeed, leftSpeed):

        # for right side of drivetrain
        if (rightSpeed > 0) and (leftSpeed > 0):  # for going forward
            self.pi_rpwmf.ChangeDutyCycle(rightSpeed)  # drive right side forward
            self.pi_lpwmf.ChangeDutyCycle(leftSpeed)
        elif (rightSpeed < 0) and (leftSpeed < 0):  # for going backward
            self.pi_rpwmb.ChangeDutyCycle(abs(rightSpeed))
            self.pi_lpwmb.ChangeDutyCycle(abs(leftSpeed))
        elif (rightSpeed > 0) and (leftSpeed < 0):  # for point turn right
            self.pi_rpwmf.ChangeDutyCycle(rightSpeed)
            self.pi_lpwmb.ChangeDutyCycle(abs(leftSpeed))
        elif (rightSpeed < 0) and (leftSpeed > 0):  # for point turn left
            self.pi_rpwmb.ChangeDutyCycle(abs(rightSpeed))
            self.pi_lpwmf.ChangeDutyCycle(leftSpeed)
        elif (rightSpeed == 0) and (leftSpeed > 0):  # for swing turn right
            self.pi_rpwmf.ChangeDutyCycle(0)
            self.pi_rpwmb.ChangeDutyCycle(0)
            self.pi_lpwmf.ChangeDutyCycle(leftSpeed)
        elif (rightSpeed > 0) and (leftSpeed == 0):  # for swing turn left
            self.pi_rpwmf.ChangeDutyCycle(rightSpeed)
            self.pi_lpwmf.ChangeDutyCycle(0)
            self.pi_lpwmb.ChangeDutyCycle(0)
        else:  # making robot stop
            self.pi_lpwmf.ChangeDutyCycle(0)
            self.pi_lpwmb.ChangeDutyCycle(0)
            self.pi_rpwmf.ChangeDutyCycle(0)
            self.pi_rpwmb.ChangeDutyCycle(0)

    def limit(self, val, minVal, maxVal):
        return min(max(val, minVal), maxVal)

    def point_turn_IMU(self, wantedAngle, speed):
        # relativePointAngle = wantedAngle - self.IMU.euler_from_quaternion()   # self.IMU.angleWrap(wantedAngle - currentAngle)

        while (self.IMU.euler_from_quaternion() > wantedAngle + self.align_threshold or self.IMU.euler_from_quaternion()
               < wantedAngle - self.align_threshold):
            # turn_speed = max(turn_speed, 50.0)
            # print("error", abs(wantedAngle-currentAngle))
            if wantedAngle > 0:
                self.drive(-speed, speed)
            else:
                self.drive(speed, -speed)

            print("desired angle: ", wantedAngle)
            print("current angle: ", self.IMU.euler_from_quaternion())

        self.drive(0, 0)

    def swing_turn_IMU(self, currentAngle, wantedAngle, decelerationAngle, speed):
        relativePointAngle = wantedAngle - currentAngle  # self.IMU.angleWrap(wantedAngle - currentAngle)
        turn_speed = (relativePointAngle / decelerationAngle) * speed
        turn_speed = self.limit(turn_speed, -speed, speed)
        turn_speed = max(turn_speed, 50.0)
        if relativePointAngle > 0:
            self.drive(0, turn_speed)
        else:
            self.drive(turn_speed, 0)

    # duration in millis
    def driveStraightIMU(self, straightSpeed, curr_angle):
        # destination = self.current_milli_time() + duration  # calculate time when destination is reached
        target = curr_angle

        # while self.current_milli_time() < destination:  # while destination has not been reached

        # if(self.IMU.angleWrap(sensor.euler[0]) != None):
        #    absolute = self.IMU.angleWrap(sensor.euler[0])#getGyro() #continue reading gyro
        # else:
        #    absolute = 0
        absolute = self.IMU.euler_from_quaternion()
        leftSpeed = straightSpeed - (absolute - target)  # adjust motor speeds
        rightSpeed = straightSpeed + (absolute - target)
        # print(rightSpeed, leftSpeed, absolute)
        self.drive(rightSpeed, leftSpeed)  # write to chassis

        # self.drive(0, 0)  # stop when arrived at destination

    def current_milli_time(self):
        return round(time.time() * 1000)
