from base_comm import TCP_COMM
from apriltag_detection import AprilTag
import sys
sys.path.insert(0, '/home/pi/beachbots2020/Code/support')

import Constants

small_bot = TCP_COMM(Constants.TCP_IP, Constants.TCP_PORT, Constants.BUFFER_SIZE)
april_tag_recognizer = AprilTag(Constants.RIGHT_ARPILTAG, Constants.LEFT_ARPILTAG, Constants.BACK_ARPILTAG, small_bot)

while True:
    april_tag_recognizer.detect_tag()
    smallbot_action = april_tag_recognizer.get_action()
    print(smallbot_action)
    small_bot.send_data(smallbot_action)
small_bot.close_conn()
