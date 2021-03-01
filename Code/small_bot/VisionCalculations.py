from Chassis import Chassis
from time import sleep
from sympy import symbols, Eq, solve

RPWMF = 22  # PWM
RPWMB = 29

LPWMF = 31  # PWM
LPWMB = 36

#chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB)

class Calculations:

    def positionCorrection(self):#, area):
        # For loop runs 5 times
        # Reasoning... ...
        # The area of the bounding box will constantly change while bot is still, 
        # therefore it is almost impossible to be 100% accurate. Number of itterations 
        # for complete accuracy is still 'up for grabs'.
	    # Initialize important variables        
        currentDist = [0] * 2	    
        y = symbols('area')
        eq = Eq(106.15*area**2 - 1564.5*area + 7804.2)
        currentDist = solve(eq)
        print(currentDist)
'''
            if(currentDist[0] < 'Desired'):     # If closer to object than needed, move back
                Chassis.drive(chassis, -10, -10)
                sleep(1)
                Chassis.drive(chassis, 0, 0)
            elif(currentDist[0] > 'Desired'):   # If farther from object than needed, move forward
                Chassis.drive(chassis, 10, 10)
                sleep(1)
                Chassis.drive(chassis, 0, 0)        
'''
#Test Distance Equation... ...
# y = 106.15x^2 - 1564.5x + 7804.2
# where....
#      x = distance from camera
#      y = area of the object
