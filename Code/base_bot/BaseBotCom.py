# title           :BaseBotCom.py
# description     :TCP Communication for the client side to send and receive data from and to the smallbot
# author          :Dennis Chavez Romero
# date            :2020-02-13
# version         :0.1
# notes           :Original source: https://wiki.python.org/moin/TcpCommunication
# python_version  :2.7
# ==============================================================================
import socket

class TCP_COMM:
    def __init__(self, TCP_IP, TCP_PORT, BUFFER_SIZE):
        """
        Class constructor
        """

        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE

        self.small_bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.small_bot.connect((TCP_IP, TCP_PORT))
        self.data_received = ""

    def send_data(self, new_data):
        """
        Sends data to the smallbot
        :param new_data     [string]  The action for the smallbot to perform next.
        """

        # Send the data to the smallbot
        self.small_bot.send(new_data)

        # Get the echo from the smallbot
        data = self.small_bot.recv(self.BUFFER_SIZE)

        # Echo from data received
        self.data_received = data
        print("received data:", data)

    def is_done_turning(self):
        """
        Checks the current echo from the smallbot received data
        :return     [string] The echo received data from the smallbot
        """

        return self.data_recieved

    def close_conn(self):
        """
        Ends the connection with the server aka the smallbot
        """
        self.small_bot.close()
