# --------------------- CONSTANTS FOR SMALLBOT ---------------------

# Right PWM Wheel Pins
RPWMF = 22
RPWMB = 29

# Left PWM Wheel Pins
LPWMF = 31
LPWMB = 36

# Max Bucket Capacity (Bottles & Cans)
MAX_BUCKET_CAPACITY = 4

# Alignment Threshold for Turning (Degrees)
DEG_THRESHOLD = 1.5

# Stepper Motor Pins
DIR = 38
STEP = 35

# Stepper Motor Degrees/Step
STEP_ANGLE = 0.035

# Pin for Limit Switch
SWITCH = 13

# Servo Controller Pins
ELBOW = 0
GRIPPER = 1
BUCKET = 2

# Servo Values for Poses
DOWN_POSE_ELBOW = 3200
MID_POSE_ELBOW = 6500
UP_POSE_ELBOW = 8000

# Servos Pre-determined
GRIPPER_OPEN_VAL = 8400
GRIPPER_CLOSED_VAL = 5900

BUCKET_DISPOSE_VAL = 7500
BUCKET_DEFAULT_VAL = 4900

# Vision Constants
MODEL_FOLDER_NAME = 'BottlesCan_model'

# Tell Vision Inference Whether or not to Use the Google Coral
USE_HARDWARE_ACCEL = True

# Camera Smallbot Resolution for OpenCV
RESOLUTION = "640x360"

# Smallbot Camera Viewing Angle
VIEW_ANGLE = 60

# Constants for DriveDetect.py
MOTOR_SPEED = 20
# in pixels
OPENCV_Y_VAL = 168
Y_VAL_THRESHOLD = 5

# --------------------- CONSTANTS FOR BASEBOT ---------------------

RIGHT_ARPILTAG = 'tag25h7'
LEFT_ARPILTAG = 'tag36h11'
BACK_ARPILTAG = 'tag25h9'


# One by default: Will drive in zig-zag manner for one lap
NUMBER_LAPS = 1

LAP_STATES = ['TURN_RIGHT', 'CREEP_FORWARD', 'TURN_RIGHT', 'FORWARD',\
              'TURN_LEFT', 'CREEP_FORWARD', 'TURN_LEFT', 'FORWARD']

BEGINNING_STATES = ['FORWARD']

END_STATES = ['TURN_RIGHT', 'CREEP_BACKWARD', 'TURN_LEFT', 'BACKWARDS', 'HALT', 'DUMP', 'STOP']

INIT_STATES = ['STARTUP', 'TURN_RIGHT_INDEF', 'ALIGN_LEFT_TAG', 'TURN_RIGHT', 'DRIVE_DIST', 'TURN_LEFT', 'DRIVE_X_BOUND']

# Actual Distance of the Apriltag When Pointed 0.6 Meters Away From the Camera
KNOWN_DISTANCE = 0.6
# Width of the Apriltag in Pixels When Pointed 0.6 Meters Away From the Camera
KNOWN_PXL_WIDTH = 170
# Width of the Apiltag in Meters
KNOWN_WIDTH = 0.1651
# Distance to Travel Forward in Inches
FWD_TRAVEL_DIST = 5
# Left-side of Camera Bounds for Start
MAX_CAM_X_BOUND_START = 130
# Left-side of Camera Bounds / Right-side of Camera Bounds for Start
MIN_CAM_X_BOUND = 120
# Right-side of Camera Bounds
MAX_CAM_X_BOUND = 520
# OpenCV Threshold Values for X Bounds
X_BOUND_THRESHOLD = 15
# Lower bound for optimal starting distance in inches
MIN_START_DISTANCE = 70
# Upper bound for optimal starting distance in inches
MAX_START_DISTANCE = 80
# --------------------- TCP esp32_wifi Parameters ---------------------
TCP_IP = '192.168.137.210'  # '192.168.4.2'
TCP_PORT = 5005
BUFFER_SIZE = 20