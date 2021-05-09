# title           :Encoder.py
# description     :Counts and updates the encoder position for both of the back wheels.
# author          :Dennis Chavez Romero
# date            :2021-04-16
# version         :0.1
# notes           :
# python_version  :3.7
# ==============================================================================
import RPi.GPIO as GPIO

class Encoder:
    def __init__(self, CHANNEL_A, CHANNEL_B):
        """"
        Class constructor
        """
        # Set encoder pins
        self.CHANNEL_A = CHANNEL_A
        self.CHANNEL_B = CHANNEL_B

        # Set global vars
        self.encoder_pos = 0
        self.encoder_pin_A_last = GPIO.LOW
        self.n = GPIO.LOW

        # Setup pins as IN for input
        GPIO.setup(self.CHANNEL_A, GPIO.IN)
        GPIO.setup(self.CHANNEL_B, GPIO.IN)

    def update_enc_count(self):

        self.n = GPIO.input(self.CHANNEL_A)

        if (self.encoder_pin_A_last is GPIO.LOW) and (self.n is GPIO.HIGH):
            if GPIO.input(self.CHANNEL_B) is GPIO.LOW:
                self.encoder_pos -= 1
            else:
                self.encoder_pos += 1

        self.encoder_pin_A_last = self.n
        
        print(self.encoder_pos)
        
        

    def get_enc_reading(self):
        return self.encoder_pos

    def reset_enc_count(self):
        self.encoder_pos = 0
