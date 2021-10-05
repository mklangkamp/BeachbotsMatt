# title           :RunSmallBot.py
# description     :Cleans trash seen and drives predetermined path received from the BaseBot
# author          :Dennis Chavez Romero, Spencer Gregg
# date            :2021-03-07
# version         :0.1
# notes           :
# python_version  :3.7
# ==============================================================================
# from Chassis import Chassis
# from SmallBotCom import TCP_COMM
# from DriveDetect import DriveDetect
import RPi.GPIO as GPIO
from pynput.keyboard import Listener # For keypress listening
from pynput.keyboard import Key
from time import sleep
import sys
sys.path.insert(0, '/home/pi/beachbots2020/Code/support')
import Constants
import keyboard

# Set PWM pins for motors
RPWMF = Constants.RPWMF  # RIGHT PWM FORWARDS
RPWMB = Constants.RPWMB  # RIGHT PWM BACKWARDS
LPWMF = Constants.LPWMF  # LEFT PWM FORWARDS
LPWMB = Constants.LPWMB  # LEFT PWM BACKWARDS

# Disable warnings
GPIO.setwarnings(False)

# Set pin numbering system
GPIO.setmode(GPIO.BOARD)

# Setup pins as OUT for output
GPIO.setup(RPWMF, GPIO.OUT)
GPIO.setup(RPWMB, GPIO.OUT)
GPIO.setup(LPWMF, GPIO.OUT)
GPIO.setup(LPWMB, GPIO.OUT)

# Create PWM instance with frequency
pi_rpwmf = GPIO.PWM(RPWMF, 1000)
pi_rpwmb = GPIO.PWM(RPWMB, 1000)
pi_lpwmf = GPIO.PWM(LPWMF, 1000)
pi_lpwmb = GPIO.PWM(LPWMB, 1000)

# Start PWM of required Duty Cycle
pi_rpwmf.start(0)
pi_rpwmb.start(0)
pi_lpwmf.start(0)
pi_lpwmb.start(0)

# Instance of chassis
# chassis = Chassis(Constants.RPWMF, Constants.RPWMB, Constants.LPWMF, Constants.LPWMB, Constants.STEP, Constants.DIR,
#                   Constants.SWITCH, Constants.GRIPPER, Constants.ELBOW, Constants.BUCKET)

# # Instance of DriveDetect class
# driveDetect = DriveDetect(chassis, Constants.RESOLUTION, Constants.VIEW_ANGLE)

# # Instance of basebot
# base_bot = TCP_COMM(Constants.TCP_IP, Constants.TCP_PORT, Constants.BUFFER_SIZE)

# # Starting variables before cleanup
# current_state = b'none'

# finished_clean = False

print('before')
keyboard.wait('up')
print('after')


leftSpeed = 0
rightSpeed = 0

def on_press(key): # Callback function for keypress
    global leftSpeed
    global rightSpeed
#    print(key)


    if(key == Key.space):#Stop if space is pressed
        leftSpeed = 0
        rightSpeed = 0

    elif(key == Key.up): #Increase speed
        if(leftSpeed == rightSpeed): # already driving forwards or backwards
            leftSpeed = leftSpeed + 5
            rightSpeed = rightSpeed + 5

    elif(key == Key.down): # Decrease speed
        if(leftSpeed == rightSpeed): # already driving forwards or backwards
            leftSpeed = leftSpeed - 5
            rightSpeed = rightSpeed - 5

    elif(key == Key.left): #decrease left, increase right
        leftSpeed = leftSpeed - 5
        rightSpeed = rightSpeed + 5

    elif(key == Key.right): #increase left, decrease right
        leftSpeed = leftSpeed + 5
        rightSpeed = rightSpeed - 5
    else:
	leftSpeed = 0
	rightSpeed = 0

    if(leftSpeed >= 100):
	leftSpeed = 100
    if(leftSpeed <= -100):
	leftSpeed = -100

    if(rightSpeed >= 100):
	rightSpeed = 100
    if(rightSpeed <= -100):
	rightSpeed = -100
    print(str(leftSpeed) + '\t' + str(rightSpeed))

    #Speed control
    if(leftSpeed < 0):
        pi_lpwmf.ChangeDutyCycle(0)
        pi_lpwmb.ChangeDutyCycle(abs(leftSpeed))
    else:
        pi_lpwmf.ChangeDutyCycle(leftSpeed)
        pi_lpwmb.ChangeDutyCycle(0)

    if(rightSpeed < 0):
        pi_rpwmf.ChangeDutyCycle(0)
        pi_rpwmb.ChangeDutyCycle(abs(rightSpeed))
    else:
        pi_rpwmf.ChangeDutyCycle(rightSpeed)
        pi_rpwmb.ChangeDutyCycle(0)
    #print(str(leftSpeed) + '\t' + str(rightSpeed))


with Listener(on_press = on_press) as listener: #Create listener, and start it 
    listener.join()


#print("Stop: Spacebar, Increase Speeds: Up Arrow, Decrease Speeds: Down Arrow, Left: Left Arrow, Right: Right Arrow")