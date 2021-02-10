from Chassis import Chassis
from AdafruitIMU import AdafruitIMU

RPWMF = 22  # PWM
RPWMB = 29

LPWMF = 31  # PWM
LPWMB = 36
chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB)
itteration = 0

#Driving test starts here... ...
while(itteration <= 0):
    Chassis.driveStraightGyro(chassis, 50, 1000)
    itteration = itteration + 1


