from base_comm import TCP_COMM
from april_tag_recognition import AprilTag

TCP_IP = '192.168.4.2'
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

right_tag = "tag36h11"
lef_tag = "tagStandard41h12"
back_tag = "tagStandard52h13"

small_bot = TCP_COMM(TCP_IP, TCP_PORT, BUFFER_SIZE)
april_tag_recognizer = AprilTag(right_tag, lef_tag, back_tag)

while True:
    april_tag_recognizer.detect_tag()
    april_tag_pos = april_tag_recognizer.get_action()
    print(april_tag_pos)
    small_bot.send_data(april_tag_pos)
