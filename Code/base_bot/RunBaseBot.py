# title           :RunBaseBot.py
# description     :Determines the smallbots actions and sends them over via TCP
# author          :Dennis Chavez Romero
# date            :2021-03-18
# version         :0.1
# notes           :Original source: https://wiki.python.org/moin/TcpCommunication
# python_version  :2.7
# ==============================================================================
from BaseBotCom import TCP_COMM
from StateMachine import StateMachine
from StartAlignment import StartAlignment
import sys
sys.path.insert(0, '/home/bob/beachbots2020/Code/support')
import Constants

# Create instances of smallbot and the state machine
small_bot = TCP_COMM(Constants.TCP_IP, Constants.TCP_PORT, Constants.BUFFER_SIZE)
go_to_start = StartAlignment(Constants.RIGHT_ARPILTAG, Constants.LEFT_ARPILTAG, Constants.BACK_ARPILTAG, small_bot)
state_machine = StateMachine(Constants.RIGHT_ARPILTAG, Constants.LEFT_ARPILTAG, Constants.BACK_ARPILTAG, small_bot)

# As long as the connection does not end
while True:
    if not go_to_start.is_ready_for_path():
        go_to_start.run_init_alignment()

        # Determine the action the smallbot should perform next
        smallbot_action = go_to_start.get_action()

        print(smallbot_action)
        # Send that action via TCP
        small_bot.send_data(smallbot_action)
    else:
        # Execute the state machine
        state_machine.run_state_machine()

        # Determine the action the smallbot should perform next
        smallbot_action = state_machine.get_action()

        print(smallbot_action)
        # Send that action via TCP
        small_bot.send_data(smallbot_action)

# Once done, close the TCP connection
small_bot.close_conn()
