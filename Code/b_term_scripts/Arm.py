import RPi.GPIO as GPIO
import time
from time import sleep

class Arm:

    def __init__(self, STEP, DIR):
        self.STEP = STEP
        self.DIR = DIR
        self.shoulder_current = 0.0
        self.STEP_ANGLE = 0.035  # Degrees per step
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        self.usleep = lambda x: time.sleep(x/1000000.0)

    def move_shoulder(self, angle):

        target = angle - self.shoulder_current
        steps = abs(int(target // self.STEP_ANGLE))
        num_steps = 0
        print("target: ", target)
        print("steps: ", steps)

        if target < 0:
            GPIO.output(self.DIR, GPIO.HIGH)
        else:
            GPIO.output(self.DIR, GPIO.LOW)
        while num_steps < steps:
            GPIO.output(SM_STEP, GPIO.HIGH)
            self.usleep(500)
            GPIO.output(SM_STEP, GPIO.LOW)
            self.usleep(500)
            num_steps += 1

        #sleep(1000)
