import RPi.GPIO as GPIO
import time
from AdafruitIMU import AdafruitIMU
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055
from time import sleep

i2c = I2C(1)
sensor = adafruit_bno055.BNO055_I2C(i2c)
class Chassis:

    def __init__(self, RPWMF, RPWMB, LPWMF, LPWMB):
        self.RPWMF = RPWMF
        self.RPWMB = RPWMB
        self.LPWMF = LPWMF
        self.LPWMB = LPWMB
        self.IMU = AdafruitIMU()

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

        #for right side of drivetrain
        if (rightSpeed > 0) & (leftSpeed > 0): #if speed is postive
            self.pi_rpwmf.ChangeDutyCycle(rightSpeed) #drive right side forward
#            self.pi_lpwmf.ChangeDutyCycle(0)
#	    self.pi_rpwmf.ChangeDutyCycle(0)
            self.pi_lpwmf.ChangeDutyCycle(leftSpeed)
        elif rightSpeed < 0: #if speed is negative
            self.pi_rpwmb.ChangeDutyCycle(abs(rightSpeed)) #drive right side backwards
            self.pi_lpwmb.ChangeDutyCycle(0)
#        elif leftSpeed > 0:
#            self.pi_rpwmf.ChangeDutyCycle(0)
#            self.pi_lpwmf.ChangeDutyCycle(leftSpeed)
        elif leftSpeed < 0:
            self.pi_rpwmb.ChangeDutyCycle(0)
            self.pi_lpwmb.ChangeDutyCycle(abs(leftSpeed))
        else:
            self.pi_lpwmf.ChangeDutyCycle(0)
            self.pi_lpwmb.ChangeDutyCycle(0)
            self.pi_rpwmf.ChangeDutyCycle(0)
            self.pi_rpwmb.ChangeDutyCycle(0)

    def estop(self):
        self.pi_rpwmf.ChangeDutyCycle(0)
        self.pi_lpwmf.ChangeDutyCycle(0)
        self.pi_rpwmb.ChangeDutyCycle(0)
        self.pi_lpwmb.ChangeDutyCycle(0)

    '''
    def turn_left(self, time, speed): #Turn is the angle at which one wants tu turn bot
        for x in range(time):
            self.pi_rpwmf.ChangeDutyCycle(speed)
            self.pi_lpwmb.ChangeDutyCycle(speed)

    def turn_right(self, time, speed): #Turn is the angle at which one wants tu turn bot
        for x in range(time):
            self.pi_rpwmb.ChangeDutyCycle(speed)
            self.pi_lpwmf.ChangeDutyCycle(speed)

    def turn(self, time, speed):
        if speed > 0: #Turn right
            for x in range(time):
                self.pi_rpwmb.ChangeDutyCycle(speed)
                self.pi_lpwmf.ChangeDutyCycle(speed)

        elif speed < 0: #Turn left
            for x in range(time):
                self.pi_rpwmf.ChangeDutyCycle(abs(speed))
                self.pi_lpwmb.ChangeDutyCycle(abs(speed))

        else:
            self.pi_rpwmf.ChangeDutyCycle(0)
            self.pi_lpwmf.ChangeDutyCycle(0)
            self.pi_rpwmb.ChangeDutyCycle(0)
            self.pi_lpwmb.ChangeDutyCycle(0)

    def set_motor_power(self, right, left):
        self.pi_rpwmf.ChangeDutyCycle(right)
        self.pi_lpwmf.ChangeDutyCycle(left)
        self.pi_rpwmb.ChangeDutyCycle(right)
        self.pi_lpwmb.ChangeDutyCycle(left)
    '''


    def limit(self, val, minVal, maxVal):
        return min(max(val, minVal), maxVal)

    def point_turn_IMU(self, currentAngle, wantedAngle, decelerationAngle, speed):
        relativePointAngle = self.IMU.angleWrap(wantedAngle - currentAngle)
        turn_speed = (relativePointAngle / decelerationAngle) * speed
        turn_speed = self.limit(turn_speed, -speed, speed)
        turn_speed = max(turn_speed, 50.0)
        self.drive(-turn_speed, turn_speed)

    def swing_turn_IMU(self, currentAngle, wantedAngle, decelerationAngle, speed):
        relativePointAngle = self.IMU.angleWrap(wantedAngle - currentAngle)
        turn_speed = (relativePointAngle / decelerationAngle) * speed
        turn_speed = self.limit(turn_speed, -speed, speed)
        turn_speed = max(turn_speed, 50.0)
        if relativePointAngle > 0:
            self.drive(0, turn_speed)
        else:
            self.drive(turn_speed, 0)

    '''
    def drive_IMU(self, currentAngle, wantedAngle, decelerationAngle, speed):
        relativePointAngle = self.angleWrap(wantedAngle - currentAngle)
        turn_speed = (relativePointAngle / decelerationAngle) * speed
        turn_speed = self.limit(turn_speed, -speed, speed)
        turn_speed = max(turn_speed, 50.0)
    '''

    #duration in millis
    def driveStraightGyro(self, straightSpeed, duration):
        destination = self.current_milli_time() + duration #calculate time when destination is reached
        target = 0

        while self.current_milli_time() < destination: #while destination has not been reached
	    
            if(self.IMU.angleWrap(sensor.euler[0]) != None): 
                absolute = self.IMU.angleWrap(sensor.euler[0])#getGyro() #continue reading gyro
            else: 
                absolute = 0
            rightSpeed = straightSpeed - (absolute - target) #adjust motor speeds
            leftSpeed = straightSpeed + (absolute - target)
            #print(rightSpeed, leftSpeed)
            print(self.IMU.angleWrap(sensor.euler[0]))
            self.drive(rightSpeed, leftSpeed) #write to chassis

        self.estop() #stop when arrived at destination

    def current_milli_time(self):
        return round(time.time() * 1000)
