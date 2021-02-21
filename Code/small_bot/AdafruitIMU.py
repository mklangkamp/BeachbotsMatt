import time
import math
import adafruit_bno055
from adafruit_extended_bus import ExtendedI2C as I2C


class AdafruitIMU:
    
    def __init__(self):
        i2c = I2C(1)  # Device is /dev/i2c-1
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        self.lastAngle = 0
        self.lastQuat = 0

        
    def angleWrap(self, angle):
        #if(angle != None):
        #    angle = angle
        #else:
        #    angle = 360.0
        if(angle == None):
            return self.lastAngle
        angle %= 180.0 #was 360
        while angle > 180.0:
            angle -= 180.0 #was 360
        while angle < -180.0:
            angle += 180.0 #was 360
        self.lastAngle = angle
        return angle

    def getAngle(self):
        angle = self.sensor.euler[0]
        return angle

    #unsure if this works
    def getGyro(self):
        gyro = self.sensor.gyro
        return gyro
    
    def getQuaternion(self):
        quat = self.sensor.quaternion
        return quat

    def euler_from_quaternion(self):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        x = self.sensor.quaternion[0]
        y = self.sensor.quaternion[1]
        z = self.sensor.quaternion[2]
        w = self.sensor.quaternion[3]

        if(not all(self.sensor.quaternion) or w == None or x == None or y == None or z == None):
            return self.lastAngle
        #print(w)
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)

        roll_x = math.degrees(roll_x)
        pitch_y = math.degrees(pitch_y)
        yaw_z = math.degrees(yaw_z)
        if roll_x > 0:
            roll_x -= 180
        elif roll_x < 0:
            roll_x +=180
        if(roll_x == None):
            return self.lastAngle
        else:  
            self.lastAngle = roll_x
        return roll_x #pitch_y, yaw_z  # in degrees
