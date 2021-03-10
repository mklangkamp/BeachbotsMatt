#!/usr/bin/env python
import socket


class TCP_COMM:
    def __init__(self, TCP_IP, TCP_PORT, BUFFER_SIZE):

        self.TCP_IP = TCP_IP #'192.168.4.2'#'10.42.43.1'
        self.TCP_PORT = TCP_PORT #5005
        self.BUFFER_SIZE = BUFFER_SIZE #1024
        self.MESSAGE = " "

        self.small_bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.small_bot.connect((TCP_IP, TCP_PORT))
        self.data_recieved = ""

    def send_data(self, new_data):
        self.MESSAGE = new_data
        #self.small_bot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.small_bot.connect((self.TCP_IP, self.TCP_PORT))
        self.small_bot.send(self.MESSAGE)
        data = self.small_bot.recv(self.BUFFER_SIZE)
        self.data_recieved = data
        print("received data:", data)

    def is_done_turning(self):
        return self.data_recieved

    def close_conn(self):
        self.small_bot.close()

