import RPi.GPIO as GPIO
import time
from time import sleep

class Arm:

    def __init__(self, STEP, DIR, SWITCH):
        self.STEP = STEP
        self.DIR = DIR
        self.SWITCH = SWITCH
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.SWITCH, GPIO.IN)#, pull_up_down=GPIO.PUD_UP)
        self.usleep = lambda x: time.sleep(x/1000000.0)
        self.shoulder_current = 0.0
        self.STEP_ANGLE = 0.035 #degrees per step

    def move_shoulder_angle(self, angle):
        target = angle - self.shoulder_current
        steps = abs(int(target // self.STEP_ANGLE))
        num_steps = 0
        print("target:",  target)
        print("steps: ", steps)
        
        if target < 0:
            GPIO.output(self.DIR, GPIO.HIGH)
        else:
            GPIO.output(self.DIR, GPIO.LOW)
        while num_steps < steps:
            GPIO.output(STEP, GPIO.HIGH)
            self.usleep(500)
            GPIO.output(STEP, GPIO.LOW)
            self.usleep(500)
            num_steps += 1
            
    def move_shoulder_press(self):
        
        if not self.switch_press:
            GPIO.output(self.DIR, GPIO.LOW)

    def switch_press(self):
        pressed = GPIO.input(self.SWITCH)
        return pressed
        #print(GPIO.input(self.SWITCH))
    def pickup(self):
        self.move_shoulder_press()
        
        '''
        if direction < 0:
            GPIO.output(self.DIR, GPIO.LOW)
        else:
            GPIO.output(self.DIR, GPIO.HIGH)

        for i in range(duration):
            GPIO.output(self.STEP, GPIO.HIGH)
            self.usleep(500)
            GPIO.output(self.STEP, GPIO.LOW)
            self.usleep(500)
        '''
        #sleep(1000)
