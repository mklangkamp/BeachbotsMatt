import socket

class TCP_COMM:
    def __init__(self, TCP_IP, TCP_PORT, BUFFER_SIZE):

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
        self.data = self.conn.recv(self.BUFFER_SIZE)

        if not self.data:
            return None

        if self.data == b'turnrightnone' or self.data == b'turnleftnone':
            self.data = b'none'
        print("Recieved data:", self.data)

        self.conn.send(self.data) #echo

        return self.data

    def send_turning_confirmation(self, data):
        self.conn.send(data) #echo

    def close_conn(self):
        self.conn.close()