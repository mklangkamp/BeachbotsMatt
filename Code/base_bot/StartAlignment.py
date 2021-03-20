# title           :StartAlignment.py
# description     :Drives the smallbot to the starting position prior to path planning
# author          :Dennis Chavez Romero
# date            :2021-03-19
# version         :0.1
# notes           :
# python_version  :2.7
# ==============================================================================
from ApriltagDectector import AprilTag
import sys
sys.path.insert(0, '/home/bob/beachbots2020/Code/support')
import Constants
import random

class StartAlignment:

    def __init__(self, right_tag, left_tag, back_tag, small_bot):
        """"
        Class constructor
        """

        # Assigning variables to the apriltags on the smallbot
        self.right_tag = right_tag
        self.left_tag = left_tag
        self.back_tag = back_tag

        # Instance of the TCP communication with the smallbot
        self.small_bot = small_bot

        # Current apriltag in view
        self.current_tag = ""

        # Current action that the smallbot is performing
        self.current_action = ""

        # Instance of ApriltagDetector class used to detect apriltags on smallbot
        self.apriltag_detector = AprilTag(self.right_tag, self.left_tag, self.back_tag)

        self.initial_random_turning_dir = ''
        self.opposite_initial_random_turning_dir = ''
        self.curr_turning_dir = ''

        self.has_chosen_random_dir = False

        self.ready_for_path_planning = False

        self.initial_left_tag_angle = 0

        # Current index in the list of states for initial alignment
        self.current_state_index = 0

        # Current state the smallbot is in (Initialize to first state in the initial alignment)
        self.status = Constants.INIT_STATES[0]

        # List of states for initial alignment
        self.path_states = Constants.INIT_STATES

    def is_ready_for_path(self):
        return self.ready_for_path_planning

    def get_action(self):
        """
        Returns the current action that the smallbot needs to perform
        :return           [string]   The action that needs to be sent to the smallbot via TCP.
        """
        return self.current_action

    def is_done_turning(self):
        """
        Checks if the smallbot is done performing a turn
        """

        check = self.small_bot.is_done_turning()
        print("DONE TURNING CHECK: ", check)
        return check

    def next_state(self):
        """
        Advances to the next state in path planning
        """

        # Increases current path index
        self.current_state_index += 1

        # Retrieves the current state in the path and updates it
        self.status = self.path_states[self.current_state_index]

    def update_action(self, status, return_tag_data):
        """
        Checks if the smallbot is done performing a turn
        :param status            [string]  The current state the smallbot is in.
        :param return_tag_data   [list]  2D list of data from the apriltags seen
        """

        # Startup state
        if status == 'STARTUP':

            # Wait for user input to start
            raw_input('Press Enter to continue...')
            self.next_state()

        # Drive forward state
        elif status == 'TURN_RIGHT_INDEF':
            # Turn right until it only sees the left apriltag
            if len(return_tag_data) == 0 or (len(return_tag_data) != 1 and return_tag_data[0][0] != self.left_tag):
                self.current_action = 'turnright_indef'

            # Stop only when the left apriltag is in view
            else:
                # Reset current action for 1 iteration to avoid data overlap
                self.current_action = 'none'
                self.next_state()

        elif status == 'ALIGN_LEFT_TAG':

            if not align_left_apriltag(return_tag_data):
                self.current_action = self.curr_turning_dir
            else:
                # Reset current action for 1 iteration to avoid data overlap
                self.current_action = 'none'
                self.next_state()

        elif status == 'TURN_RIGHT':
            # Keep turning right while the smallbot is not done achieving its goal angle aka 90 deg
            if self.is_done_turning() != 'done_turning':
                self.current_action = 'turnright'
            else:
                # Reset current action for 1 iteration to avoid data overlap
                self.current_action = 'none'
                self.next_state()

        elif status == 'DRIVE_DIST':
            curr_dist_away = return_tag_data[0][3]

            if curr_dist_away < Constants.MIN_START_DISTANCE:
                self.current_action = 'drive'
            elif curr_dist_away > Constants.MAX_START_DISTANCE:
                self.current_action = 'drivebackwards'
            else:
                # Reset current action for 1 iteration to avoid data overlap
                self.current_action = 'none'
                self.next_state()

        elif status == 'TURNLEFT':
            # Keep turning right while the smallbot is not done achieving its goal angle aka -90 deg
            if self.is_done_turning() != 'done_turning':
                self.current_action = 'turnleft'
            else:
                # Reset current action for 1 iteration to avoid data overlap
                self.current_action = 'none'
                self.next_state()

        elif status == 'DRIVE_X_BOUND':
            x = return_tag_data[0][1]

            if x < Constants.MIN_CAM_X_BOUND:
                self.current_action = 'drivebackwards'
            elif x > Constants.MAX_CAM_X_BOUND_START:
                self.current_action = 'drive'
            else:
                self.current_action = 'none'
                self.ready_for_path_planning = True


    def sort_parsed_tag_data(self, tag_data):

        sorted_tag_data = sorted(tag_data, key=lambda x:(x[0]!=self.left_tag, x))

        return sorted_tag_data

    def get_random_dir(self):
        choice = random.randrange(0, 2)

        if choice == 0:
            self.initial_random_turning_dir = 'turnright_indef'
            self.opposite_initial_random_turning_dir = 'turnleft_indef'
            return self.initial_random_turning_dir
        else:
            self.initial_random_turning_dir = 'turnleft_indef'
            self.opposite_initial_random_turning_dir = 'turnright_indef'
            return self.initial_random_turning_dir

    def align_left_apriltag(self, return_tag_data):

        # Sort the parsed tag data such that the first element of the list always happens to be the
        # sub-list containing the data about the left apriltag
        # This allows to always index the 0th sub-list as the one containing the data from the left apriltag
        sorted_tag_data = self.sort_parsed_tag_data(return_tag_data)

        # Get the current angle that the left apriltag is facing w.r.t. camera
        apriltag_angle = sorted_tag_data[0][4]

        # If it is not parallel to the camera
        if apriltag_angle > 0:

            # First choose a random direction to turn towards
            if not self.has_chosen_random_dir:
                self.curr_turning_dir = self.get_random_dir()

                # Set the initial left apriltag angle equals to the starting angle
                self.initial_left_tag_angle = apriltag_angle

                # Reset flag for next iteration
                self.has_chosen_random_dir = True

            if apriltag_angle > self.initial_left_tag_angle:
                self.curr_turning_dir = self.opposite_initial_random_turning_dir
            else:
                self.curr_turning_dir = self.curr_turning_dir

            return False

        elif apriltag_angle == 0:

            return True

    def run_init_alignment(self):
        """
        Executes the state machine
        """

        # Initial check for startup state
        if self.status == 'STARTUP':
            self.update_action(self.status, None)

        # Get apriltag data from the detector
        return_tag_data = self.apriltag_detector.get_apriltag_data()

        self.update_action(self.status, return_tag_data)
