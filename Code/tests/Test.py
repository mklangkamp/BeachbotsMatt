import RPi.GPIO as GPIO
from Chassis import Chassis
from AdafruitIMU import AdafruitIMU
#from adafruit_extended_bus import ExtendedI2C as I2C
#import adafruit_bno055
from time import sleep

#i2c = I2C(1)
#sensor = adafruit_bno055.BNO055_I2C(i2c)

RPWMF = 22  # PWM
RPWMB = 29

LPWMF = 31  # PWM
LPWMB = 36
chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB)
IMU = AdafruitIMU()
itteration = 0

#Driving test starts here... ...
#while(itteration <= 0):
Chassis.driveStraightIMU(chassis, 50, 1000)
'''
    euler_angles = IMU.euler_from_quaternion()
    print(euler_angles)
    
    Chassis.point_turn_IMU(chassis, euler_angles, 10, 5, 25)
    if abs(10-euler_angles) < 0.5:
        Chassis.drive(0, 0)
        break
'''
    #itteration = itteration + 1


