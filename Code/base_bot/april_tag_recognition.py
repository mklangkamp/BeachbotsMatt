# import the necessary packages
import apriltag
#import time
import cv2


class AprilTag:
    def __init__(self, right_tag, left_tag, back_tag, small_bot):
        self.right_tag = right_tag
        self.left_tag = left_tag
        self.back_tag = back_tag
        self.small_bot = small_bot
        self.tag_families = self.right_tag + " " + self.left_tag + " " + self.back_tag
        self.cap = cv2.VideoCapture(0)
	self.cam_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) #640 pixels wide
	self.cam_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT) #480 pixels tall
        self.current_tag = ""
        self.current_action = ""
	self.options = apriltag.DetectorOptions(families=self.tag_families)
        self.detector = apriltag.Detector(self.options)	
	self.y_val_thres = 10
	self.y_val_after_turn = 0
	self.get_y_turn_val = False
	self.tags_in_view = range(5)
	self.canUpdate_act = True
	self.needs_to_drive = False
	self.first_drive = True
        
        
    
    def check_turn(self):
        check = self.small_bot.is_done_turning()
        if check == 'done_turning':
            self.needs_to_drive = True
            
        return check
    
    
    def update_action(self, x, y):
	print("CURRENT TAG IN VIEW: ",self.tags_in_view) 
	if (x <= 580 and x >= 120) and (self.current_tag == self.right_tag or self.current_tag == self.left_tag) and (self.first_drive or self.needs_to_drive):
		self.current_action = "drive"
	elif ((x < 120) and self.current_tag == self.left_tag) or (self.check_turn() != 'done_turning' and self.current_tag == self.back_tag and not self.needs_to_drive): # Point turn right 
	        self.first_drive = False
		self.current_action = "turnright"
		self.get_y_turn_val = True
	elif (x < 120) and self.current_tag == self.back_tag and self.needs_to_drive:
		if self.get_y_turn_val:
			self.y_val_after_turn = y
			#print("Y VAL AFTER TURN-------------------------------------------: ", self.y_val_after_turn)
			#time.sleep(10)
			self.get_y_turn_val = False

		self.current_action = "drive"
        
		if y < self.y_val_after_turn - self.y_val_thres:
			self.current_action = "turnright"
			self.needs_to_drive = False
			print("second turn right")
			#time.sleep(10)
    
	elif ((x < 120) and self.current_tag == self.back_tag) or (self.check_turn() != 'done_turning' and self.current_tag == self.right_tag and not self.needs_to_drive): # Point turn left 
    		self.current_action = "turnright"
	else:
		self.current_action = "none"
		
	
	'''
        if x > 500 and self.current_tag == self.right_tag:
            self.current_action = "turnright"
        elif x < 100 and self.current_tag == self.left_tag:
            self.current_action = "turnleft"
        elif x > 100 and y > 380:
            self.current_action = "stop"
        else:
            self.current_action = "middle"
	'''

    def get_action(self):
        return self.current_action

    def detect_tag(self):
        #print("detect_tag")
        # load the input image and convert it to grayscale
        #print("[INFO] loading image...")
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # define the AprilTags detector options and then detect the AprilTags
        # in the input image
        #print("[INFO] detecting AprilTags...")
        
        results = self.detector.detect(gray)
        #print("[INFO] {} total AprilTags detected".format(len(results)))
        # loop over the AprilTag detection results
        if len(results) < 1:
            self.current_tag = "none"
            self.current_action = "none"
        elif len(results) > 1:
            self.canUpdate_act = False
        elif len(results) == 1:
            self.canUpdate_act = True

        for r in results:
            cx = r.center[0]
            cy = r.center[1]
            print("x position: ", cx)
            print("y position: ", cy)
            # extract the bounding box (x, y)-coordinates for the AprilTag
            # and convert each of the (x, y)-coordinate pairs to integers
            (ptA, ptB, ptC, ptD) = r.corners
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))
            # draw the bounding box of the AprilTag detection
            cv2.line(frame, ptA, ptB, (0, 255, 0), 2)
            cv2.line(frame, ptB, ptC, (0, 255, 0), 2)
            cv2.line(frame, ptC, ptD, (0, 255, 0), 2)
            cv2.line(frame, ptD, ptA, (0, 255, 0), 2)
            # draw the center (x, y)-coordinates of the AprilTag
            (cX, cY) = (int(r.center[0]), int(r.center[1]))
            cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
            # draw the tag family on the image
            tagFamily = r.tag_family.decode("utf-8")
            cv2.putText(frame, tagFamily, (ptA[0], ptA[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #print("[INFO] tag family: {}".format(tagFamily))
            
            for i in range(len(results)):
                #print(i)
                
                self.tags_in_view[i] = tagFamily
            
            
            self.current_tag = tagFamily
            
            if self.canUpdate_act:
                self.update_action(cx, cy)

        # show the output image after AprilTag detection
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
