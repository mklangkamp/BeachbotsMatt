from Vision import Detection
from time import sleep
import time


class DriveDetect:

    def __init__(self, chassis, camera_res, camera_view_angle):
        self.chassis = chassis
        self.object_detect = Detection(camera_res)
        resW, resH = camera_res.split('x')
        self.imW, self.imH = int(resW), int(resH)
        self.desired_coords = self.imW / 2, self.imH / 2
        self.motor_speed = 20
        self.desired_y_val = 115#108
        self.align_threshold = 5
        self.viewing_ang_max = camera_view_angle/2
        self.viewing_ang_min = -camera_view_angle/2
        self.aligned_angle = 0
        self.yaw_aligned = False
        self.first_detection = True
        self.picking_up = False
        self.bottles_acquired = 0
        self.drive_start_time = 0
        self.drive_stop_time = 0
        self.drive_back_time = 0
        self.drive_forward_time = 0
        self.drive_time = 0
        self.dir_driven = ''
        #print("inside func")

    def is_full_capacity(self):
        if self.bottles_acquired >= 4:
            return True
        else:
            return False

    def is_full_capacity(self):
        if self.bottles_acquired >= 4:
            return True
        else:
            return False

    def align_chassis(self, bottle_coords):
        # global yaw_aligned
        # global aligned_angle

        # Map bottle coordinates (camera pixel values) to imu angles wrt our camera viewing angle
        # Y = (X-A)/(B-A) * (D-C) + C
        desired_angle = bottle_coords[0] / self.imW * (self.viewing_ang_max - self.viewing_ang_min) + self.viewing_ang_min
        self.picking_up = True
        # Point turn to desired angle
        if not self.yaw_aligned:
            self.chassis.point_turn_IMU(desired_angle, self.motor_speed)
            self.aligned_angle = self.chassis.IMU.euler_from_quaternion()
            self.yaw_aligned = True
            self.drive_start_time = time.time()
            self.drive_back_time = 0
            self.drive_forward_time = 0
            self.drive_time = 0

        # print("turning...")

        # Once chassis is aligned with the bottle
        # Drive straight/backwards until the bottle is within a given y-axis threshold
        #print("y-axis bootle coordinates: ", bottle_coords[1])
        #print("upper align threshold: ", (self.desired_y_val + self.align_threshold))
        #print("lower align threshold: ", (self.desired_y_val - self.align_threshold))
        if bottle_coords[1] < (self.desired_y_val - self.align_threshold):
            # drive forward
            self.chassis.driveStraightIMU(self.motor_speed, self.aligned_angle)
            self.dir_driven = 'forward'
            print("driving forward for alignement")
            self.drive_back_time = time.time() - self.drive_start_time
            print("time to drive backwards: ", self.drive_back_time)
        elif bottle_coords[1] > (self.desired_y_val + self.align_threshold):
            # drive backwards
            self.chassis.driveStraightIMU(-self.motor_speed, self.aligned_angle)
            self.dir_driven = 'backwards'
            print("driving backwards for alignement")
            self.drive_forward_time = -(time.time() - self.drive_start_time)
            print("time to drive forwards: ", self.drive_forward_time)
        else:
            # Once the y-axis is aligned
            # Stop driving
            print("ALIGNED")
            self.drive_stop_time = time.time()
            self.drive_time = self.drive_back_time + self.drive_forward_time
            
            if self.drive_time < 0:
                self.drive_time = abs(self.drive_time)
            elif self.drive_time > 0:
                self.drive_time = self.drive_time
            
            print("time to drive back/forward: ", self.drive_time)
            self.chassis.drive(0, 0)
            return True

        return False

    def drive_back(self):
        if self.dir_driven == 'forward':
            updated_speed = -self.motor_speed
        elif self.dir_driven == 'backwards':
            updated_speed = self.motor_speed
        else:
            updated_speed = 0
            
        end_time = time.time() + self.drive_time
        while(time.time() < end_time):
            self.chassis.driveStraightIMU(updated_speed, self.aligned_angle)
            
        self.aligned_angle = 0
        self.chassis.point_turn_IMU(self.aligned_angle, self.motor_speed)
                                    
        #self.chassis.drive(0,0)

    def cleanLitter(self):

        # Run vision
        self.object_detect.detect_litter()

        # Keep driving straight with heading of 0 deg
        if not self.picking_up:
            self.chassis.driveStraightIMU(self.motor_speed, 0)
            #print("driving straight w heading of  0 ..")

        # If camera sees a bottle
        #print("current object: ", self.object_detect.get_current_object())
        
        if self.object_detect.get_current_object() == 'bottle':

            # First come to a full stop
            if self.first_detection:
                self.chassis.drive(0, 0)
                sleep(2)
                self.first_detection = False

            # Get the bottle coordinates wrt to the camera
            bottle_coords = self.object_detect.get_centroid()

            # Align the chassis and pick up
            if self.align_chassis(bottle_coords):
                print("pick up")
                self.chassis.arm.pickup()
                self.bottles_acquired += 1
                self.first_detection = True
                self.yaw_aligned = False
                self.picking_up = False
                self.drive_back()
        else:
            self.picking_up = False
