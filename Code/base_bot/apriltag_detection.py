# import the necessary packages
import apriltag
# import time
import cv2


class AprilTag:
    def __init__(self, right_tag, left_tag, back_tag, small_bot):
        self.right_tag = right_tag
        self.left_tag = left_tag
        self.back_tag = back_tag
        self.small_bot = small_bot
        self.tag_families = self.right_tag + " " + self.left_tag + " " + self.back_tag
        self.cap = cv2.VideoCapture(0)
        self.cam_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # 640 pixels wide
        self.cam_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 480 pixels tall
        # actual distance of the apriltag when pointed 0.6m away from the camera
        KNOWN_DISTANCE = 0.6
        # width of the apiltag in meters
        self.KNOWN_WIDTH = 0.1651
        # width of the apriltag in pixels when pointed 0.6m away from the camera
        KNOWN_PXL_WIDTH = 170
        self.focalLength = (KNOWN_PXL_WIDTH * KNOWN_DISTANCE) / self.KNOWN_WIDTH
        self.current_tag = ""
        self.current_action = ""
        self.options = apriltag.DetectorOptions(families=self.tag_families)
        self.detector = apriltag.Detector(self.options)

        self.current_state_index = 0
        self.path_states = 'FORWARD', 'TURN_RIGHT', 'CREEP_FORWARD', 'TURN_RIGHT', 'FORWARD', 'TURN_LEFT', 'CREEP_FORWARD', 'TURN_LEFT', 'FORWARD','TURN_RIGHT','CREEP_BACKWARD','TURN_LEFT','BACKWARDS','HALT','DUMP','STOP'
        self.times_driven_forward = self.path_states.count('CREEP_FORWARD')
        self.status = 'FORWARD'

        self.dist_to_travel = 5 # in inches
        self.dist_after_turn = 0 # in inches
        self.tags_in_view = []
        # self.canUpdate_act = True
        
    def distance_to_camera(self, perWidth):
	# compute and return the distance from the maker to the camera in inches
	if perWidth == 0:
	        return None
        return ((self.KNOWN_WIDTH * self.focalLength) / perWidth)*39.37
        

    def is_done_turning(self):
        check = self.small_bot.is_done_turning()
        print("DONE TURNING CHECK: ", check)
        return check 


    def next_state(self):
        self.current_state_index += 1
        self.status = self.path_states[self.current_state_index]

    def update_action(self, status, x, y, dist_in):
        # print("TAGS IN VIEW:", self.tags_in_view)
        print("CURRENT STATE:", self.status)
        print("DISTANCE IN IN: ", dist_in)

        if status == 'STARTUP':
            raw_input('Press Enter to continue...')
            self.next_state()

        elif status == 'FORWARD':
            if 550 >= x >= 120 and (self.current_tag == self.left_tag or self.current_tag == self.right_tag):
                self.current_action = "drive"
            else:
                self.next_state()
                
        elif status == 'BACKWARDS':
            if x <= 550 and (self.current_tag == self.left_tag or self.current_tag == self.right_tag):
                self.current_action = "drivebackwards"
            else:
                self.next_state()
                
        elif status == 'TURN_RIGHT':
            if self.is_done_turning() != 'done_turning':
                self.current_action = 'turnright'
            else:
		self.current_action = 'none'
                self.dist_after_turn = dist_in
		print("CAPTURED DIST: ", self.dist_after_turn)
                self.next_state()

        elif status == 'CREEP_FORWARD':
            print("current Y VAL AT Y: ", y)
            # 70.45 < 70.45 + 6 == 70.45 < 76.45
            if (dist_in < self.dist_after_turn + self.dist_to_travel) and self.current_tag == self.back_tag:
                self.current_action = "drive"
		print("INSIDE IF STATMT----CURRENT Y VAL: ", y)
            else:
		print("----------GONE TO NEXT STATE----------")
                self.next_state()

        elif status == 'TURN_LEFT':
            print("INSIDE TURN LEFT")
            if self.is_done_turning() != 'done_turning':
                self.current_action = 'turnleft'
            else:
		self.current_action = 'none'
                self.dist_after_turn = dist_in
                print("CAPTURED DIST: ", self.dist_after_turn)
                self.next_state()
        
        elif status == 'CREEP_BACKWARD':
            print("current Y VAL AT Y: ", y)
            if (dist_in > self.dist_after_turn - (self.dist_to_travel*self.times_driven_forward)) and self.current_tag == self.back_tag:
                self.current_action = "drivebackwards"
		print("INSIDE IF STATMT----CURRENT Y VAL: ", y)
            else:
		print("----------GONE TO NEXT STATE----------")
                self.next_state()

        elif status == 'STOP':
            self.current_action = 'stop'
        
        elif status == 'HALT':
            self.current_action = 'stop' 
            self.next_state()
            
        elif status == 'DUMP':
            self.current_action = 'dump'
            self.next_state()

        else:
            self.current_action = 'none'

    def get_action(self):
        return self.current_action

    def detect_tag(self):
        # print("detect_tag")
        # load the input image and convert it to grayscale
        # print("[INFO] loading image...")
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # define the AprilTags detector options and then detect the AprilTags
        # in the input image
        # print("[INFO] detecting AprilTags...")

        results = self.detector.detect(gray)
        # print("[INFO] {} total AprilTags detected".format(len(results)))
        # loop over the AprilTag detection results
        '''
        if len(results) < 1:
            self.current_tag = "none"
            self.current_action = "none"
        elif len(results) > 1:
            self.canUpdate_act = False
        elif len(results) == 1:
            self.canUpdate_act = True
        '''
        # print("TAGS IN VIEW:", self.tags_in_view)

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
            # print("[INFO] tag family: {}".format(tagFamily))
            pxl_width = int(ptB[0])-int(ptA[0])
            dist_in = self.distance_to_camera(pxl_width)
            
            # del self.tags_in_view[:]
            '''
            for i in range(len(results)):
                self.tags_in_view.append(tagFamily)
            '''    
            # if self.canUpdate_act:
            self.current_tag = tagFamily
            
            if self.status == 'CREEP_FORWARD' and (tagFamily == self.back_tag):
                print("ATTEMPTING TO UPDATE STATUS 1")
                self.update_action(self.status, cx, cy, dist_in)
            if self.status == 'CREEP_FORWARD' and (tagFamily == self.right_tag):
                print("ATTEMPTING TO UPDATE STATUS 2")
                pass
            else:
                print("ATTEMPTING TO UPDATE STATUS 3")
                self.update_action(self.status, cx, cy, dist_in)

        # show the output image after AprilTag detection
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
