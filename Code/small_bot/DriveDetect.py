from Vision import Detection
from time import sleep


class DriveDetect:

    def __init__(self, chassis, camera_res):
        self.chassis = chassis
        self.object_detect = Detection(camera_res)
        resW, resH = camera_res.split('x')
        self.imW, self.imH = int(resW), int(resH)
        self.desired_coords = self.imW / 2, self.imH / 2
        self.motor_speed = 20
        self.desired_y_val = 108
        self.align_threshold = 5
        self.viewing_ang = 60
        self.aligned_angle = 0
        self.yaw_aligned = False
        self.first_detection = True
        self.bottles_acquired = 0

    def align_chassis(self, bottle_coords):
        # global yaw_aligned
        # global aligned_angle

        # Map bottle coordinates (camera pixel values) to imu angles wrt our camera viewing angle
        # Y = (X-A)/(B-A) * (D-C) + C
        desired_angle = bottle_coords[0] / self.imW * self.viewing_ang / 2

        # Point turn to desired angle
        if not self.yaw_aligned:
            self.chassis.point_turn_IMU(desired_angle, self.motor_speed)
            self.aligned_angle = self.chassis.IMU.euler_from_quaternion()
            self.yaw_aligned = True

        # print("turning...")

        # Once chassis is aligned with the bottle
        # Drive straight/backwards until the bottle is within a given y-axis threshold
        if bottle_coords[1] < (self.desired_y_val - self.align_threshold):
            # drive forward
            self.chassis.driveStraightIMU(self.motor_speed, self.aligned_angle)
        elif bottle_coords[1] > (self.desired_y_val + self.align_threshold):
            # drive backwards
            self.chassis.driveStraightIMU(-self.motor_speed, self.aligned_angle)
        else:
            # Once the y-axis is aligned
            # Stop driving
            print("ALIGNED")
            self.chassis.drive(0, 0)
            return True

        return False

    def drive_back(self):
        # TODO: make the robot drive back and face its original heading
        pass

    def cleanLitter(self):

        # Run vision
        self.object_detect.detect_litter()

        # Keep driving straight with heading of 0 deg
        self.chassis.driveStraightIMU(self.motor_speed, 0)

        # If camera sees a bottle
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
                self.chassis.arm.pickup()
                self.bottles_acquired += 1
                self.first_detection = True
                self.yaw_aligned = False
                self.drive_back()