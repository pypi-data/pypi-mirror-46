"""A small package for sending and recieving commands per tcp
   commands: connect() connects to the server
             send() sends a message/command to the server
             recieve() recieves a message/command from the server
"""
import socket
import sys
class telnet():
    def __init__(self, ip, port=23):
        """
        Define the server adress and the port
        example: server = telnet.telnet('127.0.0.1', 2000)
                 server = telnet.telnet('127.0.0.1') standard port is 23
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = (ip, port)
    def connect(self):
        """connect to the server"""
        self.client.connect(self.server)
    def send(self, cmd, form="UTF-8"):
        """send a message/command to the server
        example: server.send('say hello', 'UTF-16')
                 server.send('say hello') standard is UTF-8
        """
        self.client.send(bytes(cmd, form))
    def recieve(self, bytess):
        """recieve a message/command from the server
        example: server.recieve(1024) number of bytes
        """
        return str(self.client.recv(bytess), 'UTF-8')