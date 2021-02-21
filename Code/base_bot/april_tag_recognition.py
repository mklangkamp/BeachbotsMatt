# import the necessary packages
import apriltag
import argparse
import cv2
#from imutils import paths
import imutils
#import socket

''' THIS DOESN'T WORK WELL
def find_marker(image):
	# convert the image to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
	# find the contours in the edged image and keep the largest one;
	# we'll assume that this is our piece of paper in the image
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key = cv2.contourArea)
	# compute the bounding box of the of the paper region and return it
	return cv2.minAreaRect(c)'''


class AprilTag:
		def __init__(self, distance, width):
			self.KNOWN_DISTANCE = distance
			self.KNOWN_WIDTH = width
			self.focalLength = (300 * KNOWN_DISTANCE) / KNOWN_WIDTH
			# construct the argument parser and parse the arguments
			ap = argparse.ArgumentParser()
			# ap.add_argument("-i", "--image", required=True,
			#	help="path to input image containing AprilTag")
			args = vars(ap.parse_args())

		def distance_to_camera(self, per_width):
			# compute and return the distance from the maker to the camera
			return (self.KNOWN_WIDTH * self.focalLength) / per_width
		'''
		def meters_to_inches(self, current):
			return current*39.37
		'''

		def detect_tag(self):

			cap = cv2.VideoCapture(0)

			# load the input image and convert it to grayscale
			#print("[INFO] loading image...")
			ret, frame = cap.read()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			# define the AprilTags detector options and then detect the AprilTags
			# in the input image
			#print("[INFO] detecting AprilTags...")
			options = apriltag.DetectorOptions(families="tag36h11") #"tag36h11"
			#options = at.DetectorOptions(families="tagStandard41h12")
			detector = apriltag.Detector(options)
			results = detector.detect(gray)

			#print("[INFO] {} total AprilTags detected".format(len(results)))

			#Only when no april tags are seen, assume "middle" case
			cap.release()

			# loop over the AprilTag detection results
			for r in results:
				cx = r.center[0]
				cy = r.center[1]
				print("x position: ", cx)
				print("y position: ", cy)

				if cx > 500:
					return "turnright"
				elif cx < 100:
					return "turnleft"
				elif cx > 100 and cy > 380:
					return "stop"
				elif cx > "someNUM" and cy > "someNUM":  # only when front/back Apriltags are seen
					return "drive"
				else:
					return "middle"
