#from vision import VideoStream
from Vision import Detection
#from Arm import Arm
#from Testy import Testy

# Objects
object_detect = Detection()
#test = Testy()
#arm = Arm()

while True:
    object_detect.detect_litter()
    
    if object_detect.get_current_object() == 'cup':
        print(object_detect.get_current_object())
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
