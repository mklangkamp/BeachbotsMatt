# title           :StateMachine.py
# description     :Runs the state machine used for path planning
# author          :Dennis Chavez Romero, Spencer Gregg
# date            :2021-03-18
# version         :0.1
# notes           :
# python_version  :2.7
# ==============================================================================
from ApriltagDectector import AprilTag
import sys
sys.path.insert(0, '/home/bob/beachbots2020/Code/support')
import Constants


class StateMachine:

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

        # List of states for path planning
        self.path_states = []

        # Current index in the list of states for path planning
        self.current_state_index = 0

        # Used to determine how far back the smallbot needs to drive when returning to starting position
        self.times_driven_forward = 0

        # Current state the smallbot is in (Initialize to first state in the path)
        self.status = Constants.BEGINNING_STATES[0]

        # Distance in inches that the back apriltag is in after a turn
        self.dist_after_turn = 0  #

        # Instance of ApriltagDetector class used to detect apriltags on smallbot
        self.apriltag_detector = AprilTag(self.right_tag, self.left_tag, self.back_tag)

    def calculate_path(self):
        """
        Determines the states needed for a full path based on the number of laps input.
        """

        mid_states = []

        # Add in between states
        for i in range(Constants.NUMBER_LAPS):
            mid_states = mid_states + Constants.LAP_STATES

        # Concatenate beginning, middle and end states to obtain full path of states
        self.path_states = Constants.BEGINNING_STATES + mid_states + Constants.END_STATES

        # Determine the amount of times that the smallbot will drive forward during the path
        self.times_driven_forward = self.path_states.count('CREEP_FORWARD')

        print("Calculated path: ", self.path_states)

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

    def update_action(self, status, x, y, dist_in):
        """
        Main logic for state machine. Updates the data to be sent to the smallbot

        :param status     [string]  The current state the smallbot is in.
        :param x          [float]   The OpenCV x position from the current apiltag in view.
        :param y          [float]   The OpenCV y position from the current apiltag in view.
        :param dist_in    [float]   The distance in inches of the current apriltag in view from the camera.
        """
        print("CURRENT STATE:", self.status)
        print("DISTANCE IN IN: ", dist_in)

        # Startup state
        if status == 'STARTUP':
            # Determine the states needed for our path
            self.calculate_path()

            # Wait for user input to start
            raw_input('Press Enter to continue...')
            self.next_state()

        # Drive forward state
        elif status == 'FORWARD':
            # If the current apriltag in view is either the smallbot's right or left tag
            # and the current apriltag's x position is within the camera bounds
            if (x < Constants.MAX_CAM_X_BOUND and x > Constants.MIN_CAM_X_BOUND) and \
                    (self.current_tag == self.left_tag or self.current_tag == self.right_tag):
                self.current_action = "drive"
            else:
                # Reset current action for 1 iteration to avoid data overlap
                self.current_action = 'none'
                print("DONE DRIVING STRAIGHT---------------------------------")
                self.next_state()

        # Drive backwards state
        elif status == 'BACKWARDS':
            # If the current apriltag in view is either the smallbot's right or left tag
            # and as long as the apriltag's x position is less than or equal to the max camera bound
            if (x <= Constants.MAX_CAM_X_BOUND) and \
                    (self.current_tag == self.left_tag or self.current_tag == self.right_tag):
                self.current_action = "drivebackwards"
            else:
                self.next_state()

        # Turn right state
        elif status == 'TURN_RIGHT':
            # Keep turning right while the smallbot is not done achieving its goal angle aka 90 deg
            if self.is_done_turning() != 'done_turning':
                self.current_action = 'turnright'
            else:
                # Reset current action for 1 iteration to avoid data overlap
                self.current_action = 'none'
                # Capture the current apriltag's distance from the camera after turn
                self.dist_after_turn = dist_in
                print("CAPTURED DIST: ", self.dist_after_turn)
                self.next_state()

        # Turn left state
        elif status == 'TURN_LEFT':
            print("INSIDE TURN LEFT")
            # Keep turning left while the smallbot is not done achieving its goal angle aka -90 deg
            if self.is_done_turning() != 'done_turning':
                self.current_action = 'turnleft'
            else:
                # Reset current action for 1 iteration to avoid data overlap
                self.current_action = 'none'
                # Capture the current apriltag's distance from the camera after turn
                self.dist_after_turn = dist_in
                print("CAPTURED DIST: ", self.dist_after_turn)
                self.next_state()

        # Creep forward state
        elif status == 'CREEP_FORWARD':
            print("current Y VAL AT Y: ", y)
            # If it sees the back apriltag then keep going straight for the defined TRAVEL_DIST
            if (dist_in < self.dist_after_turn + Constants.FWD_TRAVEL_DIST) and self.current_tag == self.back_tag:
                self.current_action = "drive"
                print("INSIDE IF STATMT----CURRENT Y VAL: ", y)
            else:
                print("----------GONE TO NEXT STATE----------")
                self.next_state()

        # Creep backwards state
        elif status == 'CREEP_BACKWARD':
            print("current Y VAL AT Y: ", y)
            # If it sees the back apriltag then keep going backwards for the defined
            # TRAVEL_DIST times the number of times it creeped forward
            if (dist_in > self.dist_after_turn - (
                    Constants.FWD_TRAVEL_DIST * self.times_driven_forward)) and self.current_tag == self.back_tag:
                self.current_action = "drivebackwards"
                print("INSIDE IF STATMT----CURRENT Y VAL: ", y)
            else:
                print("----------GONE TO NEXT STATE----------")
                self.next_state()

        # Halt state
        elif status == 'HALT':
            # First stop
            self.current_action = 'stop'
            # Then go to next state
            self.next_state()

        # Dump state
        elif status == 'DUMP':
            self.current_action = 'dump'
            self.next_state()

        # Stop state
        elif status == 'STOP':
            self.current_action = 'stop'

        # Default state
        else:
            self.current_action = 'none'

    def get_action(self):
        """
        Returns the current action that the smallbot needs to perform
        :return           [string]   The action that needs to be sent to the smallbot via TCP.
        """
        return self.current_action

    def run_state_machine(self):
        """
        Executes the state machine
        """

        # Initial check for startup state
        if self.status == 'STARTUP':
            self.update_action(self.status, None, None, None)
        # Get apriltag data from the detector

        return_tag_data = self.apriltag_detector.get_apriltag_data()

        # Check if it saw an apriltag
        if len(return_tag_data) != 0:

            # Iterate over the data from each of the apriltags seen
            for i in range(len(return_tag_data)):

                # Temp apriltag data
                temp_tag = return_tag_data[i]

                print("current state: ", self.status)

                print("Statemachine x VAL: ", temp_tag[1])

                print("Statemachine y VAL: ", temp_tag[2])

                # If the smallbot is currently in the CREEP_FORWARD state
                # handle cases for when the camera sees the side tags while it is driving forward
                if self.status == 'CREEP_FORWARD' and (temp_tag[0] == self.back_tag):
                    self.current_tag = temp_tag[0]
                    print("ATTEMPTING TO UPDATE STATUS 1")
                    self.update_action(self.status, temp_tag[1], temp_tag[2], temp_tag[3])
                # Ignore cases when the camera sees the side apriltags
                elif self.status == 'CREEP_FORWARD' and (temp_tag[0] == self.right_tag):
                    print("ATTEMPTING TO UPDATE STATUS 2")
                    pass
                elif self.status == 'CREEP_FORWARD' and (temp_tag[0] == self.left_tag):
                    print("ATTEMPTING TO UPDATE STATUS 2")
                    pass
                else:
                    self.current_tag = temp_tag[0]
                    print("ATTEMPTING TO UPDATE STATUS 3")
                    self.update_action(self.status, temp_tag[1], temp_tag[2], temp_tag[3])

        # If the camera did not see any apriltags
        else:
            self.current_tag = None
            self.update_action(None, None, None, None)
