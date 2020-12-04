import RPi.GPIO as GPIO
import time
from time import sleep

class Arm:

    def __init__(self, STEP, DIR):
        self.STEP = STEP
        self.DIR = DIR
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        self.usleep = lambda x: time.sleep(x/1000000.0)

    def move_shoulder(self, direction, duration):

        if direction < 0:
            GPIO.output(self.DIR, GPIO.LOW)
        else:
            GPIO.output(self.DIR, GPIO.HIGH)

        for i in range(duration):
            GPIO.output(self.STEP, GPIO.HIGH)
            self.usleep(500)
            GPIO.output(self.STEP, GPIO.LOW)
            self.usleep(500)

        #sleep(1000)
