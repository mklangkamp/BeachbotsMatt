import sys
print(sys.path)
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
import keyboard
import time

def key_press(key):
    print(key.name + '\n')

keyboard.on_press(key_press)

while True:
    time.sleep(1)
