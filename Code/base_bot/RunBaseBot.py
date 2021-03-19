from base_comm import TCP_COMM
from StateMachine import StateMachine
import sys
sys.path.insert(0, '/home/bob/beachbots2020/Code/support')
import Constants

small_bot = TCP_COMM(Constants.TCP_IP, Constants.TCP_PORT, Constants.BUFFER_SIZE)
state_machine = StateMachine(Constants.RIGHT_ARPILTAG, Constants.LEFT_ARPILTAG, Constants.BACK_ARPILTAG, small_bot)

while True:
    state_machine.run_state_machine()
    smallbot_action = state_machine.get_action()
    print(smallbot_action)
    small_bot.send_data(smallbot_action)
small_bot.close_conn()
