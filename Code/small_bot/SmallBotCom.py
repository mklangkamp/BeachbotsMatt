# title           :BaseBotCom.py
# description     :TCP esp32_wifi for the server side to receive data from the basebot
# author          :Dennis Chavez Romero
# date            :2021-02-13
# version         :0.1
# notes           :Original source: https://wiki.python.org/moin/TcpCommunication
# python_version  :3.7
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

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(1)

        self.data = ''

        self.conn, self.addr = self.s.accept()
        print('Connection address:', self.addr)

    def get_data(self):
        """
        Gets data from the basebot
        :return data     [string]  The action for the smallbot to perform next.
        """

        # Capture data from basebot
        self.data = self.conn.recv(self.BUFFER_SIZE)

        if not self.data:
            return None

        # Handling corner cases when turning
        # Since after sending a turning confirmation will cause an overlap of data received
        # we want to change this for readability purposes
        if self.data == b'turnrightnone' or self.data == b'turnleftnone':
            self.data = b'none'

        print("Recieved data:", self.data)

        # Echo
        self.conn.send(self.data)

        return self.data

    def send_turning_confirmation(self, data):
        """
        Sends unrequested echos to the basebot as a means to transmit information about when the smallbot is done
        turning -- Do not do this unless strictly necessary

        :return data     [string]  Confirmation message of whether or not a turn has been completed.
        """
        self.conn.send(data) #echo

    def close_conn(self):
        """
        Ends the connection with the server aka the smallbot
        """
        self.conn.close()
