#from vision import VideoStream
from Vision import Detection
from VisionCalculations import Calculations
from Chassis import Chassis
from Arm import Arm
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

desired_y_val = 175
align_threshold = 15
viewing_ang = 75
yaw_aligned = False

chassis = Chassis(RPWMF, RPWMB, LPWMF, LPWMB, STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET)
arm = Arm(STEP, DIR, SWITCH, GRIPPER, ELBOW, BUCKET)
#test = Testy()
#arm = Arm()

def align_chassis(bottle_coords):
    global yaw_aligned

    if not yaw_aligned:
        desired_angle = (bottle_coords[0])/(imW) * viewing_ang - (viewing_ang/2)
    else:
        desired_angle = chassis.IMU.euler_from_quaternion()

    while (chassis.IMU.euler_from_quaternion() > desired_angle + align_threshold or chassis.IMU.euler_from_quaternion() 
    < desired_angle - align_threshold):

        #point turn to desired angle
        chassis.point_turn_IMU(desired_angle, desired_angle-5, 80)

    yaw_aligned = True

    if bottle_coords[1]<(desired_y_val-align_threshold):
        #drive forward
        chassis.drive(80,80)
    elif bottle_coords[1]>(desired_y_val+align_threshold):
        #drive backwards
        chassis.drive(-80,-80)
    else:
        print("ALIGNED")
        chassis.drive(0,0)
        return True
    
    return False
        
        

'''
while True:
    object_detect.detect_litter()
    
    if object_detect.get_current_object() == 'bottle':
        
        print(object_detect.get_current_object())
        print(object_detect.get_current_object_area())
        bottle_coords = object_detect.get_current_center()
        print(bottle_coords)
        if align_chassis(bottle_coords):
            break
'''
arm.pickup(False)        

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
