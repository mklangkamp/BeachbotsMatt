# title           :ApriltagDetector.py
# description     :Detects apriltags within the camera view
# author          :Dennis Chavez Romero, Spencer Gregg
# date            :2021-02-18
# version         :0.1
# notes           :Source code for apriltag detection
#                  obtained from: https://www.pyimagesearch.com/2020/11/02/apriltag-with-python/
# python_version  :2.7
# ==============================================================================
import apriltag
import cv2
import sys

sys.path.insert(0, '/home/bob/beachbots2020/Code/support')
import Constants


class AprilTag:
    def __init__(self, right_tag, left_tag, back_tag):
        """"
        Class constructor
        """

        # Assigning tag families to detect based on the apriltags on the smallbot
        self.tag_families = right_tag + " " + left_tag + " " + back_tag

        # Video source for OpenCV
        self.cap = cv2.VideoCapture(0)

        # Camera resolution (width and height)
        self.cam_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # 640 pixels wide
        self.cam_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 480 pixels tall

        # Calculate camera's focal length
        self.focalLength = (Constants.KNOWN_PXL_WIDTH * Constants.KNOWN_DISTANCE) / Constants.KNOWN_WIDTH

        # Options and detector objects for apriltag detector
        self.options = apriltag.DetectorOptions(families=self.tag_families)
        self.detector = apriltag.Detector(self.options)

        # Values for the fitted tag pixel width & height
        self.curr_tag_width = 0
        self.curr_tag_height = 0

        # Apriltag data from the tags within camera view
        self.apriltag_tag_data = []

    def calculate_apriltag_angle(self):
        """
        Calculates an apriltag's tilt angle relative from the camera
        Source: https://github.com/ariwasch/OpenCV-Distance-Angle-Demo
        :return    [int] Angle (in degrees) about the z-axis of an apriltag in relation to the camera.
        """
        if(Constants.KNOWN_WIDTH != 0 and self.curr_tag_height > self.curr_tag_width):
            angle = (1 - (self.fitted_width/self.fitted_height)) * 90
        else:
            angle = 0

        return angle

    def calculate_euclidean_distance(self, x1, y1, x2, y2):
        """
        Calculates the distance from 2 coordinate points
        :param x1      [int] x1 point.
        :param y1      [int] y1 point.
        :param x2      [int] x2 point.
        :param y2      [int] y2 point.
        :return:       [int] Euclidean distance between 2 coordinates points.
        """
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return dist

    def distance_to_camera(self, perWidth):
        """
        Computes and return the distance from an apriltag to the camera in inches
        :param perWidth       [int]    The amount of pixel per width of the current apriltag in view.
        :return               [float]  The distance in incnes from the apriltag to the camera.
        """

        if perWidth == 0:
            return None
        return ((Constants.KNOWN_WIDTH * self.focalLength) / perWidth) * 39.37

    def split_tags_seen(self, tag_data, num_of_tags):
        """
        Parses a string of apriltag data into usable lists
        :param tag_data         [list]  The apriltag data received from the ApriltagDetector class.
        :param num_of_tags      [int]   The number of apriltags that were seen by the detector.
        :return                 [list]  2D list of data from the apriltags seen
        """

        # Return None if no apriltags were seen
        if num_of_tags == 0:
            return None

        avg = len(tag_data) / float(num_of_tags)
        out = []
        last = 0.0

        # Split the list of apriltag data to separate sub-lists
        while last < len(tag_data):
            out.append(tag_data[int(last):int(last + avg)])
            last += avg

        return out

    def get_apriltag_data(self):
        """
        Returns parsed, usable lists of apriltag data
        :return                 [list]  2D list of data from the apriltags seen
        """
        # Update the apriltag data
        self.detect_tags()

        return self.apriltag_tag_data

    def detect_tags(self):
        """
        Detects apriltags within the camera view
        """
        # Temp list of apriltag data
        tags_seen = []
        # Load the input image and convert it to grayscale
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Define the AprilTags detector options and then detect the AprilTags in the input image
        results = self.detector.detect(gray)
        # Determine the number of apriltags that it detected
        num_tags_seen = len(results)
        # Loop over the AprilTag detection results

        for r in results:
            cx = r.center[0]
            cy = r.center[1]
            print("x position: ", cx)
            print("y position: ", cy)

            # extract the bounding box (x, y)-coordinates for the AprilTag
            # and convert each of the (x, y)-coordinate pairs to integers
            (ptA, ptB, ptC, ptD) = r.corners

            # Top-left point
            ptB = (int(ptB[0]), int(ptB[1]))

            # Top-right point
            ptC = (int(ptC[0]), int(ptC[1]))

            # Bottom-right point
            ptD = (int(ptD[0]), int(ptD[1]))

            # Bottom-left point
            ptA = (int(ptA[0]), int(ptA[1]))

            # draw the bounding box of the AprilTag detection

            # Left line
            cv2.line(frame, ptA, ptB, (0, 255, 0), 2)

            # Top line
            cv2.line(frame, ptB, ptC, (0, 255, 0), 2)

            # Right line
            cv2.line(frame, ptC, ptD, (0, 255, 0), 2)

            # Bottom line
            cv2.line(frame, ptD, ptA, (0, 255, 0), 2)

            # Calculate current apriltag's pixel width and height
            self.curr_tag_width = self.calculate_euclidean_distance(ptA[0], ptA[1], ptB[0], ptB[1])
            self.curr_tag_height = self.calculate_euclidean_distance(ptB[0], ptB[1], ptC[0], ptC[1])

            # draw the center (x, y)-coordinates of the AprilTag
            (cX, cY) = (int(r.center[0]), int(r.center[1]))
            cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)

            # draw the tag family on the image
            tagFamily = r.tag_family.decode("utf-8")
            cv2.putText(frame, tagFamily, (ptA[0], ptA[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Calculate pixel width of the apriltag
            pxl_width = int(ptB[0]) - int(ptA[0])

            # Calculate distance away from the camera in in ches
            dist_in = self.distance_to_camera(pxl_width)

            # Calculate angle about the z-axis of the apriltag w.r.t. camera
            angle = self.calculate_apriltag_angle()

            # Append raw data to list
            tags_seen.extend((tagFamily, cx, cy, dist_in, angle))

        # Split the data up into sub-lists of each individual apriltag
        self.apriltag_tag_data = self.split_tags_seen(tags_seen, num_tags_seen)

        # show the output image after AprilTag detection
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
