'''import cv2
import numpy as np 
import apriltag as at

imagepath = 'test.jpg'
image = cv2.imread(imagepath, cv2.IMREAD_GRAYSCALE)
#detector = at.Detector("tagStandard41h12")
options = at.DetectorOptions(families="tagStandard41h12")
detector = at.Detector(options=options)

detections = detector.detect(image)'''

'''import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()'''



# import the necessary packages
import apriltag
import argparse
import cv2
#from imutils import paths
import imutils

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

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

def meters_to_inches(current):
	return current*39.37

def detect_tag_pos(x, y):
	if (x > 500):
		return "turnright"
	elif (x < 100):
		return "turnleft"
	elif x < 100 and y > 380:
		return "stop" 


# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 0.2
# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 0.0975
# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
#marker = find_marker(image)
focalLength = (300 * KNOWN_DISTANCE) / KNOWN_WIDTH


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#	help="path to input image containing AprilTag")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(0)

while(True):
	# load the input image and convert it to grayscale
	#print("[INFO] loading image...")
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	#print('width, height:',width, height)

	# define the AprilTags detector options and then detect the AprilTags
	# in the input image
	#print("[INFO] detecting AprilTags...")
	options = apriltag.DetectorOptions(families="tag36h11") #"tag36h11"
	#options = at.DetectorOptions(families="tagStandard41h12")
	detector = apriltag.Detector(options)
	results = detector.detect(gray)
	#print("[INFO] {} total AprilTags detected".format(len(results)))

	# loop over the AprilTag detection results
	for r in results:
		cx = r.center[0]
		cy = r.center[1]
		#print("x position: ", cx, "y position: ", cy)
		#print("y position: ", cy)
		print(detect_tag_pos(cx, cy))

		
		#print("Inches: ", meters_to_inches(meters))


		# extract the bounding box (x, y)-coordinates for the AprilTag
		# and convert each of the (x, y)-coordinate pairs to integers
		(ptA, ptB, ptC, ptD) = r.corners
		#print(ptA)
		#print(ptB)

		width = int(ptB[0])-int(ptA[0])

		#marker = find_marker(frame)
		meters = distance_to_camera(KNOWN_WIDTH, focalLength, width)
		xPos = distance_to_camera(KNOWN_WIDTH, focalLength, cx)
		#print("xPos: ", meters_to_inches(xPos))
		#print("Inches: ", meters_to_inches(meters))


		#print(int(ptB[0])-int(ptA[0]))
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
		cv2.putText(frame, tagFamily, (ptA[0], ptA[1] - 15),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		#print("[INFO] tag family: {}".format(tagFamily))
		# show the output image after AprilTag detection

	cv2.imshow("Image", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break

cap.release()
cv2.destroyAllWindows()

