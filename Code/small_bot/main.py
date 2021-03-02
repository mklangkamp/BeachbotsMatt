#from vision import VideoStream
from Vision import Detection
from VisionCalculations import Calculations
from Chassis import Chassis
from Arm import Arm
from time import sleep
#from Testy import Testy

# Objects
RPWMF = 22  # PWM
RPWMB = 29

LPWMF = 31  # PWM
LPWMB = 36

DIR = 38
STEP = 35
SWITCH = 13

GRIPPER = 1
ELBOW = 0
BUCKET = 2

resolution = "640x360"
object_detect = Detection(resolution)
calc = Calculations()
resW, resH = resolution.split('x')
imW, imH = int(resW), int(resH)
desired_coords = imW/2, imH/2

desired_y_val = 108
align_threshold = 5
viewing_ang_upper = 30
viewing_ang_lower = -30
aligned_angle = 0
yaw_aligned = False

chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB, STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET)
arm = Arm(STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET)
#test = Testy()
#arm = Arm()

def align_chassis(bottle_coords):
    global yaw_aligned
    global aligned_angle
    #Y = (X-A)/(B-A) * (D-C) + C
    desired_angle = (bottle_coords[0] - 0)/(imW - 0) * (viewing_ang_upper - viewing_ang_lower) + viewing_ang_lower


    #point turn to desired angle
    if not yaw_aligned:
        chassis.point_turn_IMU(desired_angle, 20)
        aligned_angle = chassis.IMU.euler_from_quaternion()
        yaw_aligned = True
    

    #print("turning...")


    if bottle_coords[1]<(desired_y_val-align_threshold):
        #drive forward
        chassis.driveStraightIMU(20, aligned_angle)
    elif bottle_coords[1]>(desired_y_val+align_threshold):
        #drive backwards
        chassis.driveStraightIMU(-20, aligned_angle)
    else:
        print("ALIGNED")
        chassis.drive(0,0)
        return True
    
    return False
        
        
first_detection = True

while True:
  
    object_detect.detect_litter()
    
    chassis.driveStraightIMU(20, 0)
    
    if object_detect.get_current_object() == 'bottle':
        
        if first_detection == True:
            chassis.drive(0,0)
            sleep(2)
            first_detection = False
            
            
        #print(object_detect.get_current_object())
        #print(object_detect.get_current_object_area())
        bottle_coords = object_detect.get_current_center()
        #print(bottle_coords)
        if align_chassis(bottle_coords):
            break
            
   

    
arm.pickup()

'''
    if(object_detect.object == 'bottle'):
        print(object_detect.object)

    # Position the bot for successfull collection        
        Tetsy.positionCorrection(test, object_detect.objectArea)
        
        # Run collection routine
        Arm.pickup(arm, 1)

    elif(object_detect.object == 'weeb'):
        print("Thats a fuckin weeb!!") 
'''
