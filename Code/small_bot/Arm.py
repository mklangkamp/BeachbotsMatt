import RPi.GPIO as GPIO
import time
from time import sleep
from ServoController import ServoController

class Arm:

    def __init__(self, STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET):
        self.STEP = STEP
        self.DIR = DIR
        self.SWITCH = SWITCH
        self.GRIPPER = GRIPPER
        self.ELBOW = ELBOW
        self.BUCKET = BUCKET
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.SWITCH, GPIO.IN)#, pull_up_down=GPIO.PUD_UP)
        self.usleep = lambda x: time.sleep(x/1000000.0)
        self.shoulder_current = 0.0
        self.STEP_ANGLE = 0.035 #degrees per step
        self.servo = ServoController(self.GRIPPER, self.ELBOW, self.BUCKET)
        self.DOWN_POSE_ELBOW = 4600 #original 5300 
        self.MID_POSE_ELBOW = 6500
        self.UP_POSE_ELBOW = 8000
        self.calibrate()
        
    def move_shoulder_angle(self, angle):
        target = angle - self.shoulder_current
        steps = abs(int(target // self.STEP_ANGLE))
        num_steps = 0
        print("target:",  target)
        print("steps: ", steps)
        print("current angle: ", self.shoulder_current)
        
        if angle < 0:
            GPIO.output(self.DIR, GPIO.LOW)
        else:
            GPIO.output(self.DIR, GPIO.HIGH)
        while num_steps < steps:
            GPIO.output(self.STEP, GPIO.HIGH)
            self.usleep(500)
            GPIO.output(self.STEP, GPIO.LOW)
            self.usleep(500)
            num_steps += 1
        self.shoulder_current += angle
        print("target:",  target)
        print("steps: ", steps)
        print("current angle: ", self.shoulder_current)

    def calibrate(self):
        self.servo.elbow(self.UP_POSE_ELBOW) #UP position for elbow
        GPIO.output(self.DIR, GPIO.LOW)
        while not GPIO.input(self.SWITCH):
            GPIO.output(self.STEP, GPIO.HIGH)
            self.usleep(500)
            GPIO.output(self.STEP, GPIO.LOW)
            self.usleep(500)
        self.shoulder_current = 0
        

    #def switch_press(self):
    #    pressed = GPIO.input(self.SWITCH)
    #    return pressed
        #print(GPIO.input(self.SWITCH))

    def pickup(self, readypick):
        if not readypick:
            self.move_shoulder_angle(45) #original 30 changed for camera 
            self.servo.gripper(True)
            self.usleep(1000)
            self.servo.elbow(self.DOWN_POSE_ELBOW)
            self.servo.get_elbow_pos()
            self.usleep(1000)
        else:
            self.servo.gripper(False)
            self.usleep(1000)
            self.move_shoulder_angle(110)
            self.servo.elbow(self.UP_POSE_ELBOW)
            self.usleep(1000)
            self.servo.gripper(True)
            self.usleep(1000)
            self.servo.elbow(self.MID_POSE_ELBOW)
            self.usleep(1000)
            self.move_shoulder_angle(30)

        
        
        #110 degrees for shoulder up, 30 degrees for down
        
        #move stepper until limit switch, open gipper, move elbow,
        #drive forward, small amount, rotate back(arm/gripper),
        #release gripper, move shoulder forward
        
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
