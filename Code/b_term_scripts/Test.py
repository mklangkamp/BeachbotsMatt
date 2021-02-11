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
while(itteration <= 0):
    #print(AdafruitIMU.angleWrap(sensor, sensor.euler[2]), sensor.euler[2])
    #print(IMU.getQuaternion())
    euler_angles = IMU.euler_from_quaternion()
    if euler_angles != None:
        print(euler_angles)
    #print(IMU.getQuaternion())
    #print(AdafruitIMU.euler_from_quaternion())
    '''
    currAngle = AdafruitIMU.angleWrap(sensor, sensor.euler[0])
    print(currAngle)
    
    Chassis.point_turn_IMU(chassis, currAngle, 15, 5, 50)
    if abs(15-currAngle) < 2:
        self.drive(0, 0)
        break
    '''
    #Chassis.driveStraightGyro(chassis, 50, 1000)
    #itteration = itteration + 1


