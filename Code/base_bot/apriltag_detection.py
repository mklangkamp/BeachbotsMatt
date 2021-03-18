# import the necessary packages
import apriltag
import cv2
import sys
sys.path.insert(0, '/home/bob/beachbots2020/Code/support')
import Constants


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
        self.focalLength = (Constants.KNOWN_PXL_WIDTH * Constants.KNOWN_DISTANCE) / Constants.KNOWN_WIDTH
        self.current_tag = ""
        self.current_action = ""
        self.options = apriltag.DetectorOptions(families=self.tag_families)
        self.detector = apriltag.Detector(self.options)

        self.current_state_index = 0
        self.path_states = []
        self.times_driven_forward = 0
        # Starting state
        self.status = Constants.BEGINNING_STATES[0]

        self.dist_after_turn = 0  # in inches
        self.tags_in_view = []
        # self.canUpdate_act = True

        self.calculate_path()

    def calculate_path(self):
        mid_states = []

        for i in range(Constants.NUMBER_LAPS):
            mid_states = mid_states + Constants.LAP_STATES

        self.path_states = Constants.BEGINNING_STATES + mid_states + Constants.END_STATES

        self.times_driven_forward = self.path_states.count('CREEP_FORWARD')

        print("Calculated path: ", self.path_states)

    def distance_to_camera(self, perWidth):
        # compute and return the distance from the maker to the camera in inches
        if perWidth == 0:
            return None
        return ((Constants.KNOWN_WIDTH * self.focalLength) / perWidth) * 39.37

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
            if (Constants.MAX_CAM_X_BOUND >= x >= Constants.MIN_CAM_X_BOUND or \
                Constants.MAX_CAM_X_BOUND + Constants.X_BOUND_THRESHOLD >= x >= Constants.MIN_CAM_X_BOUND - Constants.X_BOUND_THRESHOLD) and \
                    (self.current_tag == self.left_tag or self.current_tag == self.right_tag):
                self.current_action = "drive"
            else:
                self.next_state()

        elif status == 'BACKWARDS':
            if (x <= Constants.MAX_CAM_X_BOUND) and \
                    (self.current_tag == self.left_tag or self.current_tag == self.right_tag):
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
            if (dist_in < self.dist_after_turn + Constants.FWD_TRAVEL_DIST) and self.current_tag == self.back_tag:
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
            if (dist_in > self.dist_after_turn - (
                    Constants.FWD_TRAVEL_DIST * self.times_driven_forward)) and self.current_tag == self.back_tag:
                self.current_action = "drivebackwards"
                print("INSIDE IF STATMT----CURRENT Y VAL: ", y)
            else:
                print("----------GONE TO NEXT STATE----------")
                self.next_state()

        elif status == 'HALT':
            self.current_action = 'stop'
            self.next_state()

        elif status == 'DUMP':
            self.current_action = 'dump'
            self.next_state()

        elif status == 'STOP':
            self.current_action = 'stop'

        else:
            self.current_action = 'none'

    def get_action(self):
        return self.current_action

    def split_tags_seen(self, tag_data, num_of_tags):
        avg = len(tag_data) / float(num_of_tags)
        out = []
        last = 0.0

        while last < len(tag_data):
            out.append(tag_data[int(last):int(last + avg)])
            last += avg

        return out

    def run_state_machine(self):
        return_tag_data = self.detect_tag()
        temp_tag_data = return_tag_data[0]
        num_tags = return_tag_data[1]

        if num_tags > 0:

            parsed_tag_data = self.split_tags_seen(temp_tag_data, num_tags)

            for i in range(len(parsed_tag_data)):

                current_tag = parsed_tag_data[i]

                if self.status == 'CREEP_FORWARD' and (current_tag[0] == self.back_tag):
                    self.current_tag = current_tag[0]
                    print("ATTEMPTING TO UPDATE STATUS 1")
                    self.update_action(self.status, current_tag[1], current_tag[2], current_tag[3])
                elif self.status == 'CREEP_FORWARD' and (current_tag[0] == self.right_tag):
                    print("ATTEMPTING TO UPDATE STATUS 2")
                    pass
                elif self.status == 'CREEP_FORWARD' and (current_tag[0] == self.left_tag):
                    print("ATTEMPTING TO UPDATE STATUS 2")
                    pass
                else:
                    self.current_tag = current_tag[0]
                    print("ATTEMPTING TO UPDATE STATUS 3")
                    self.update_action(self.status, current_tag[1], current_tag[2], current_tag[3])

            else:
                self.update_action(None, None, None, None)

    def detect_tag(self):
        # print("detect_tag")
        # load the input image and convert it to grayscale
        # print("[INFO] loading image...")
        tags_seen = []
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # define the AprilTags detector options and then detect the AprilTags
        # in the input image
        # print("[INFO] detecting AprilTags...")

        results = self.detector.detect(gray)
        # print("[INFO] {} total AprilTags detected".format(len(results)))
        # loop over the AprilTag detection results
        num_tags_seen = len(results)
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
            pxl_width = int(ptB[0]) - int(ptA[0])
            dist_in = self.distance_to_camera(pxl_width)

            # del self.tags_in_view[:]
            '''
            for i in range(len(results)):
                self.tags_in_view.append(tagFamily)
            '''
            # if self.canUpdate_act:


            tags_seen.extend((tagFamily, cx, cy, dist_in))

        # show the output image after AprilTag detection
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

        return tags_seen, num_tags_seen
