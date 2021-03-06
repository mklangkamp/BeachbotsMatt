from base_comm import TCP_COMM
from april_tag_recognition import AprilTag

TCP_IP = '192.168.137.210'
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

right_tag = "tag16h5"
left_tag = "tag36h11"
back_tag = "tag25h9"

april_tag_recognizer = AprilTag(right_tag, left_tag, back_tag)
small_bot = TCP_COMM(TCP_IP, TCP_PORT, BUFFER_SIZE)
#i = 0 


while True:
    april_tag_recognizer.detect_tag()
    april_tag_pos = april_tag_recognizer.get_action()
    print(april_tag_pos)
    small_bot.send_data(april_tag_pos)
    #i += 1
small_bot.close_conn()
