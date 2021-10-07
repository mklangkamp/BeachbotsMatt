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

from time import sleep
import sys
sys.path.insert(0, '/home/pi/beachbots2020/Code/support')
import Constants
import termios
import tty

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


#Start Control code

leftSpeed = 0
rightSpeed = 0
running = True

def getChar():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
	return ch



while(running):

    charTyped = getChar()

    #When arrow keys are pressed, a series of three keypresses are registered.
    #Each arrow keypress has ASCII characters of 27, then 91, followed by either
    #A, B, C, or D. The following code is to interpret that and translate it into
    #The WASD controls already implemented.
    #27,91,65: up, 27,91,66: down, 27,91,67: right, 27,91,68: left

    #If any of the characters that are in the series of messages are pressed,
    #Check if its the determining character (A,B,C,D) otherwise return to beginning
    #Of loop to receive remainder of data (including determining character)
    if(charTyped != None and ([27,91,65,66,67,68].count(ord(charTyped)) != 0)):
        if(charTyped == "A"):
            charTyped = "w"
        elif(charTyped == "B"):
            charTyped = "s"
        elif(charTyped == "C"):
            charTyped = "d"
        elif(charTyped == "D"):
            charTyped = "a"
        else:
            continue

    #End code if z is typed
    if(charTyped == "z"):
        running = False

    #Use character typed to modify speed
    if(charTyped == "w"): #Increase speed
        leftSpeed = leftSpeed + 5
        rightSpeed = rightSpeed + 5

    elif(charTyped == "s"): # Decrease speed
        leftSpeed = leftSpeed - 5
        rightSpeed = rightSpeed - 5

    elif(charTyped == "a"): #decrease left, increase right
        leftSpeed = leftSpeed - 5
        rightSpeed = rightSpeed + 5

    elif(charTyped == "d"): #increase left, decrease right
        leftSpeed = leftSpeed + 5
        rightSpeed = rightSpeed - 5
    else:
        leftSpeed = 0
        rightSpeed = 0

    #Keep values in range of motor controllers.
    if(leftSpeed >= 100):
        leftSpeed = 100
    if(leftSpeed <= -100):
        leftSpeed = -100

    if(rightSpeed >= 100):
        rightSpeed = 100
    if(rightSpeed <= -100):
        rightSpeed = -100
    
    #If a character has been typed, update the PWM signals sent with that info. 
    if(charTyped != None):
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
        print(str(leftSpeed) + '\t' + str(rightSpeed))

        charTyped = None