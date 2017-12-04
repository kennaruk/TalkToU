import socket
import sys
import threading
from authen import *

class ThreadedClient:
    def __init__(self, host, port):
        self.serverSocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.serverConnect()
        

    def serverConnect(self):
        self.serverSocket.connect((self.host, self.port))
        self.send(self.serverSocket, AUTHEN)
        print("Server Status:")
        print(self.serverSocket.recv(12345).decode()) #Server Status

        print("Friend List:")
        self.recv() #FriendList

        print("Heartbeat Threading!")
        threading.Thread(target = self.heartbeatThread).start() #Thread HeartBeat

    def heartbeatThread(self):
        while True:
            greetingMsg = "Hello " + CLIENT['USER']
            serverRcv = self.serverSocket.recv(12345).decode()
            if greetingMsg == serverRcv:
                print(serverRcv)
                print("Hello Server")
                self.send(self.serverSocket, "Hello Server")

    def send(self, socket, msg):
        socket.send(bytes(msg, 'utf-8'))

    def recv(self):
        recv = self.serverSocket.recv(12345).decode()
        print(recv)

client = ThreadedClient("128.199.83.36", 34260)


# s = socket.socket(
#     socket.AF_INET, socket.SOCK_STREAM)

# s.connect(("128.199.83.36", 34260))

# s.send(bytes(AUTHEN, 'utf-8'))

# recv = s.recv(12345).decode() #STATUS Recieve
# print(recv)
# if recv == "404 ERROR":
#     sys.exit()

# recv = s.recv(12345).decode() #Friend List
# print(recv)
# recv = s.recv(12345).decode()
# print(recv)
# recv = s.recv(12345).decode()
# print(recv)

# while True: 
    # recv = s.recv(12345).decode()
    # if recv == "END":
        # print("END Rcv!")
        # break
    # print(recv)

# print(AUTHEN)
# print(CLIENT)