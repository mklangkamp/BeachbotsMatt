# title           :DriveDetect.py
# description     :Performs bottle/can alignment and pickup motions
# author          :Dennis Chavez Romero, Spencer Gregg, Yossef Naim
# date            :2021-02-19
# version         :0.1
# notes           :
# python_version  :3.7
# ==============================================================================
from Vision import Detection
from time import sleep
import time
import sys
sys.path.insert(0, '/home/pi/beachbots2020/Code/support')
import Constants


class DriveDetect:

    def __init__(self, chassis, camera_res, camera_view_angle):
        """
        Class constructor
        """

        # Instance of chassis
        self.chassis = chassis

        # Instance of detection for object recognition
        self.object_detect = Detection(camera_res)

        # Get width and height camera values based on resolution
        resW, resH = camera_res.split('x')
        self.imW, self.imH = int(resW), int(resH)

        # By default our desired coordinates for alignment are in the center of the camera view
        self.desired_coords = self.imW / 2, self.imH / 2

        # Calculate bounds from our camera viewing angle
        self.viewing_ang_max = camera_view_angle/2
        self.viewing_ang_min = -camera_view_angle/2

        # Class variables used for alignment
        self.aligned_angle = 0
        self.yaw_aligned = False
        self.first_detection = True
        self.picking_up = False
        self.objects_acquired = 0
        self.drive_start_time = 0
        self.drive_back_time = 0
        self.drive_forward_time = 0
        self.drive_time = 0
        self.dir_driven = ''

    def is_full_capacity(self):
        """
        Checks if the bucket is at full capacity
        :return    [bool] Boolean indicating if the amount of objects collected exceeds the max bucket capacity.
        """

        # If the number of objects collected equal the max bucket capacity
        if self.objects_acquired == Constants.MAX_BUCKET_CAPACITY:
            # Return true
            return True
        else:
            # Otherwise there is more space left
            return False

    def align_chassis(self, obj_coords):
        """
        Aligns the chassis with a set of object coordinates obtained from the camera
        :param obj_coords      [tuple] The set of x,y coordinates of the object's detected centroid.
        :return                [bool]  Boolean indicating if chassis is aligned with the object or not.
        """

        # Begin pick up process
        self.picking_up = True

        # Map object coordinates (camera pixel values) to a yaw angle w.r.t. the camera viewing angle
        # Y = (X-A)/(B-A) * (D-C) + C
        desired_angle = obj_coords[0] / self.imW * (self.viewing_ang_max - self.viewing_ang_min) + self.viewing_ang_min

        # Point turn to desired angle
        if not self.yaw_aligned:
            # Turn chassis to calculated angle
            self.chassis.point_turn_IMU(desired_angle, Constants.MOTOR_SPEED)

            # Capture current angle after yaw alignment
            self.aligned_angle = self.chassis.IMU.get_yaw()

            # Indicate that the yaw has been aligned
            self.yaw_aligned = True

            # Start timer to measure how long the chassis will have drive for
            # to align itself with object's y-axis
            self.drive_start_time = time.time()

            # Set counter variables to 0 at the start
            self.drive_back_time = 0
            self.drive_forward_time = 0
            self.drive_time = 0

        # Once chassis is aligned with the bottle
        # Drive straight/backwards until the bottle is within a given y-axis threshold

        # If the chassis is too far away from the object, then drive forward
        if obj_coords[1] < (Constants.OPENCV_Y_VAL - Constants.Y_VAL_THRESHOLD):
            self.chassis.drive_straight_IMU(Constants.MOTOR_SPEED, self.aligned_angle)

            # Set the last direction driven as forward
            self.dir_driven = 'forward'

            # Update counter to drive back once it is done aligning
            self.drive_back_time = time.time() - self.drive_start_time
            print("Time to drive backwards: ", self.drive_back_time)

        # Otherwise if the chassis is too far away from the object, then drive forward
        elif obj_coords[1] > (Constants.OPENCV_Y_VAL + Constants.Y_VAL_THRESHOLD):
            self.chassis.drive_straight_IMU(-Constants.MOTOR_SPEED, self.aligned_angle)

            # Set the last direction driven as backwards
            self.dir_driven = 'backwards'

            # Update counter to drive back once it is done aligning
            self.drive_forward_time = -(time.time() - self.drive_start_time)
            print("Time to drive forwards: ", self.drive_forward_time)

        # Once the y-axis is aligned
        # Stop driving
        else:
            print("Aligned")
            # Calculate total time to drive either backwards or forwards
            self.drive_time = self.drive_back_time + self.drive_forward_time

            # If the drive back time is negative
            if self.drive_time < 0:
                # Calculate the absolute value
                self.drive_time = abs(self.drive_time)

            # Otherwise do nothing
            elif self.drive_time > 0:
                self.drive_time = self.drive_time
            
            print("Time to drive backwards/forwards: ", self.drive_time)

            # Stop driving chassis after alignment
            self.chassis.drive(0, 0)

            # Return true once the chassis is fully aligned
            return True

        # Return false while it is not aligned
        return False

    def drive_back(self):
        """
        Drives chassis back to its original position prior to pickup and return heading to 0
        """

        # If the last direction that the chassis drove was forward
        if self.dir_driven == 'forward':
            # Then drive backwards for return
            updated_speed = -Constants.MOTOR_SPEED

        # Otherwise
        elif self.dir_driven == 'backwards':
            # Then drive forwards
            updated_speed = Constants.MOTOR_SPEED

        # Else do not drive at all
        else:
            updated_speed = 0

        # Calculate time to finish driving back based on the total driving time during the y-axis alignment
        end_time = time.time() + self.drive_time

        # While the timer is not up
        while time.time() < end_time:
            # Drive back or forward with its current heading based on the previously defined parameters
            self.chassis.drive_straight_IMU(updated_speed, self.aligned_angle)

        # Return chassis to heading of 0
        self.chassis.point_turn_IMU(0, Constants.MOTOR_SPEED)

    def clean_litter(self):
        """
        Makes the smallbot drive straight while it scans for bottles/cans to pickup, and will perform the pickup
        motions if an object is detected
        """

        # Run vision
        self.object_detect.detect_litter()

        # Keep driving straight with heading of 0 degrees
        if not self.picking_up:
            self.chassis.drive_straight_IMU(Constants.MOTOR_SPEED, 0)

        # If camera sees a bottle or a can
        if self.object_detect.get_current_object() == 'bottle' or self.object_detect.get_current_object() == 'can':

            # First come to a full stop
            if self.first_detection:
                self.chassis.drive(0, 0)
                sleep(2)
                self.first_detection = False

            # Get the object coordinates w.r.t. to the camera
            obj_coords = self.object_detect.get_centroid()

            # Once the chassis is fully aligned with the object
            if self.align_chassis(obj_coords):
                # Pickup the object
                self.chassis.arm.pickup()

                # Increase object counter
                self.objects_acquired += 1

                # Return chassis to its previous location and heading
                self.drive_back()

                # Reset detection variables once it is done
                self.first_detection = True
                self.yaw_aligned = False
                self.picking_up = False

        else:
            # Set pickup to false if it does not detect anything
            self.picking_up = False
