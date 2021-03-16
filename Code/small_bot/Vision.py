# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util
import sys

sys.path.insert(1, 'beachbots2020\Code\support')

import Constants


# Import Smallbot packages
# from Testy import Testy

# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""

    def __init__(self, resolution=(640, 360), framerate=30):  # was 640,480 framerate was 30
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])

        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

        # Variable to control when the camera is
        self.stopped = False

    def start(self):
        # Start the thread that reads frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # Return the most recent frame
        return self.frame

    def stop(self):
        # Indicate that the camera and thread should be stopped
        self.stopped = True


class Detection:
    def __init__(self, resolution):
        self.object = "test"
        self.object_area = 0.0
        MODEL_NAME = Constants.MODEL_FOLDER_NAME
        GRAPH_NAME = 'detect.tflite'  # 'edgetpu.tflite'
        LABELMAP_NAME = 'labelmap.txt'
        self.min_conf_threshold = 0.5
        self.curr_object = ''
        self.coordinates = 0, 0
        current_res = resolution  # '512x512'
        resW, resH = current_res.split('x')
        self.imW, self.imH = int(resW), int(resH)
        use_TPU = True

        # Import TensorFlow libraries
        # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
        # If using Coral Edge TPU, import the load_delegate library
        # ---------------------------------TEST AGAIN-------------------------------------------
        pkg = importlib.util.find_spec('tflite_runtime')
        # if pkg:
        from tflite_runtime.interpreter import Interpreter
        # if use_TPU:
        from tflite_runtime.interpreter import load_delegate
        '''else:
            from tensorflow.lite.python.interpreter import Interpreter
            if use_TPU:
                from tensorflow.lite.python.interpreter import load_delegate'''

        # If using Edge TPU, assign filename for Edge TPU model
        if use_TPU:
            # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
            if (GRAPH_NAME == 'detect.tflite'):  # 'detect.tflite'
                GRAPH_NAME = 'edgetpu.tflite'  # 'edgetpu.tflite'

        # Get path to current working directory
        CWD_PATH = os.getcwd()

        # Path to .tflite file, which contains the model that is used for object detection
        PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)

        # Path to label map file
        PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

        # Load the label map
        with open(PATH_TO_LABELS, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        # Have to do a weird fix for label map if using the COCO "starter model" from
        # https://www.tensorflow.org/lite/models/object_detection/overview
        # First label is '???', which has to be removed.
        if self.labels[0] == '???':
            del (self.labels[0])

        # Load the Tensorflow Lite model.
        # If using Edge TPU, use special load_delegate argument
        if use_TPU:
            self.interpreter = Interpreter(model_path=PATH_TO_CKPT,
                                           experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
            print(PATH_TO_CKPT)
        else:
            self.interpreter = Interpreter(model_path=PATH_TO_CKPT)

        self.interpreter.allocate_tensors()

        # Get model details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

        self.floating_model = (self.input_details[0]['dtype'] == np.float32)

        self.input_mean = 127.5
        self.input_std = 127.5

        # Initialize frame rate calculation
        self.frame_rate_calc = 1
        self.freq = cv2.getTickFrequency()

        # Initialize video stream
        self.videostream = VideoStream(resolution=(self.imW, self.imH), framerate=30).start()  # framerate was 30
        time.sleep(1)

    def get_current_object(self):
        # print("current object: ", self.curr_object)
        return self.curr_object

    def get_centroid(self):
        return self.coordinates

    def detect_litter(self):

        # for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

        # Start timer (for calculating frame rate)
        t1 = cv2.getTickCount()

        # Grab frame from video stream
        frame1 = self.videostream.read()

        # Acquire frame and resize to expected shape [1xHxWx3]
        frame = frame1.copy()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if self.floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        # Retrieve detection results
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[
            0]  # Bounding box coordinates of detected objects
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]  # Class index of detected objects
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]  # Confidence of detected objects
        # num = self.interpreter.get_tensor(self.output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)


        # Assume no detection at first
        self.curr_object = 'None'

        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > self.min_conf_threshold) and (scores[i] <= 1.0)):
                
                object_name = self.labels[int(classes[i])]  # Look up object name from "labels" array using class index
                
                if object_name != 'not': 
                    # Get bounding box coordinates and draw box
                    # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                    ymin = int(max(1, (boxes[i][0] * self.imH)))
                    xmin = int(max(1, (boxes[i][1] * self.imW)))
                    ymax = int(min(self.imH, (boxes[i][2] * self.imH)))
                    xmax = int(min(self.imW, (boxes[i][3] * self.imW)))

                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

                    # Draw centroid
                    cv2.circle(frame, (int((xmin + xmax) / 2), int((ymin + ymax) / 2)), radius=5, color=(0, 0, 255),
                               thickness=-1)

                    # Draw label

                    # Change to avoid drawing labels to 'not' objects
                    

                    if object_name == 'bottle' or object_name == 'can':
                        self.curr_object = object_name
                    else:
                        self.curr_object = 'None'

                    # self.objectArea = (xmax * ymax) / 100
                    self.coordinates = int((xmin + xmax) / 2), int((ymin + ymax) / 2)
                    # print the name of the detected object inside of the terminal for testing purposes.
                    # print(object_name)

                    label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                    label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
                    # Draw white box to put label text in
                    cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10),
                                  (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),
                                2)  # Draw label text


        # Calculate framerate
        t2 = cv2.getTickCount()
        time1 = (t2 - t1) / self.freq
        frame_rate_calc = 1 / time1

        # print(obj_name)
        # Draw framerate in corner of frame
        cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0),
                    2, cv2.LINE_AA)

        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            # Clean up
            cv2.destroyAllWindows()
            self.videostream.stop()
