import RPi.GPIO as GPIO
from time import sleep

class Chassis:

    def __init__(self, RPWMF, RPWMB, LPWMF, LPWMB):
        self.RPWMF = RPWMF
        self.RPWMB = RPWMB
        self.LPWMF = LPWMF
        self.LPWMB = LPWMB

        GPIO.setwarnings(False)  # disable warnings
        GPIO.setmode(GPIO.BOARD)  # set pin numbering system

        GPIO.setup(self.RPWMF, GPIO.OUT)
        GPIO.setup(self.RPWMB, GPIO.OUT)
        GPIO.setup(self.LPWMF, GPIO.OUT)
        GPIO.setup(self.LPWMB, GPIO.OUT)

        self.pi_rpwmf = GPIO.PWM(self.RPWMF, 1000)  # create PWM instance with frequency
        self.pi_rpwmb = GPIO.PWM(self.RPWMB, 1000)  # create PWM instance with frequency
        self.pi_lpwmf = GPIO.PWM(self.LPWMF, 1000)  # create PWM instance with frequency
        self.pi_lpwmb = GPIO.PWM(self.LPWMB, 1000)  # create PWM instance with frequency

        self.pi_rpwmf.start(0)  # start PWM of required Duty Cycle
        self.pi_rpwmb.start(0)  # start PWM of required Duty Cycle
        self.pi_lpwmf.start(0)  # start PWM of required Duty Cycle
        self.pi_lpwmb.start(0)  # start PWM of required Duty Cycle

    def drive(self, speed):
        if speed > 0:
            self.pi_rpwmf.ChangeDutyCycle(speed)
            self.pi_lpwmf.ChangeDutyCycle(speed)
        elif speed < 0:
            self.pi_rpwmb.ChangeDutyCycle(abs(speed))
            self.pi_lpwmb.ChangeDutyCycle(abs(speed))

    def estop(self):
        self.pi_rpwmf.ChangeDutyCycle(0)
        self.pi_lpwmf.ChangeDutyCycle(0)
        self.pi_rpwmb.ChangeDutyCycle(0)
        self.pi_lpwmb.ChangeDutyCycle(0)