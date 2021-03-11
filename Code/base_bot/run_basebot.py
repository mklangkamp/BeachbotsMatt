from base_comm import TCP_COMM
from apriltag_detection import AprilTag

TCP_IP = '192.168.137.210'#'192.168.4.2' ---current working w hotspot ip
TCP_PORT = 5005
BUFFER_SIZE = 1024

'''
# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 0.2
# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 0.0975
'''

right_tag = "tag25h7"
left_tag = "tag36h11"
back_tag = "tag25h9"

small_bot = TCP_COMM(TCP_IP, TCP_PORT, BUFFER_SIZE)
april_tag_recognizer = AprilTag(right_tag, left_tag, back_tag, small_bot)

while True:
    april_tag_recognizer.detect_tag()
    smallbot_action = april_tag_recognizer.get_action()
    print(smallbot_action)
    small_bot.send_data(smallbot_action)
small_bot.close_conn()
