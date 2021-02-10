import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055


class AdafruitIMU:
    
    def __init__(self):
        i2c = I2C(1)  # Device is /dev/i2c-1
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        self.lastAngle = 0
        
    def angleWrap(self, angle):
        #if(angle != None):
        #    angle = angle
        #else:
        #    angle = 360.0
        if(angle == None):
            return self.lastAngle
        angle %= 360.0
        while angle > 180.0:
            angle -= 360.0
        while angle < -180.0:
            angle += 360.0
        self.lastAngle = angle
        return angle

    def getAngle(self):
        angle = self.sensor.euler[0]
        return angle

    #unsure if this works
    def getGyro(self):
        gyro = self.sensor.gyro[0]
        return gyro
