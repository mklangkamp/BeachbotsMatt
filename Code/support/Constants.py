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
GRIPPER = 1
ELBOW = 0
BUCKET = 2

# Servo Values for Poses
DOWN_POSE_ELBOW = 3200
MID_POSE_ELBOW = 6500
UP_POSE_ELBOW = 8000

# Servos Pre-determined
GRIPPER_OPEN_VAL = 8400
GRIPPER_CLOSE_VAL = 5900

BUCKET_DISPOSE_VAL = 7500
BUCKET_DEFAULT_VAL = 4900

# Vision Constants
MODEL_FOLDER_NAME = 'BottlesCan_model'

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

# --------------------- TCP Communication Parameters ---------------------
TCP_IP = '192.168.137.210'  # '192.168.4.2'
TCP_PORT = 5005
BUFFER_SIZE = 20