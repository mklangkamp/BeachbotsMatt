from base_comm import TCP_COMM
from apriltag_detection import AprilTag
from support.Constants import *

small_bot = TCP_COMM(TCP_IP, TCP_PORT, BUFFER_SIZE)
april_tag_recognizer = AprilTag(RIGHT_ARPILTAG, LEFT_ARPILTAG, BACK_ARPILTAG, small_bot)

while True:
    april_tag_recognizer.detect_tag()
    smallbot_action = april_tag_recognizer.get_action()
    print(smallbot_action)
    small_bot.send_data(smallbot_action)
small_bot.close_conn()
