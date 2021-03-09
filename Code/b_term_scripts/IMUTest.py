import time
from AdafruitIMU import *
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055

i2c = I2C(1)  # Device is /dev/i2c-1
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:
    print(sensor.euler[0])
