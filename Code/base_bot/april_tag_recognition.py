# import the necessary packages
import apriltag
import cv2


class AprilTag:
    def __init__(self, right_tag, left_tag, back_tag):
        self.right_tag = right_tag
        self.left_tag = left_tag
        self.back_tag = back_tag
        self.tag_families = self.right_tag + " " + self.left_tag + " " + self.back_tag
        self.cap = cv2.VideoCapture(0)
        self.current_tag = ""
        self.current_action = ""
        print("running")

    def update_action(self, x, y):
        if x > 500 and self.current_tag == self.right_tag:
            self.current_action = "turnright"
        elif x < 100 and self.current_tag == self.left_tag:
            self.current_action = "turnleft"
        elif x > 100 and y > 380:
            self.current_action = "stop"
        else:
            self.current_action = "middle"

    def get_action(self):
        return self.current_action

    def detect_tag(self):
        print("detect_tag")
        # load the input image and convert it to grayscale
        #print("[INFO] loading image...")
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # define the AprilTags detector options and then detect the AprilTags
        # in the input image
        #print("[INFO] detecting AprilTags...")
        options = apriltag.DetectorOptions(families=self.tag_families)
        detector = apriltag.Detector(options)
        results = detector.detect(gray)
        #print("[INFO] {} total AprilTags detected".format(len(results)))
        # loop over the AprilTag detection results
        if len(results) < 1:
            self.current_tag = "none"
            self.current_action = "none"

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

            self.current_tag = tagFamily
            self.update_action(cx, cy)

        # show the output image after AprilTag detection
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
