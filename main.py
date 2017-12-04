import socket
import sys
import threading
from authen import *

class ThreadedClient:
    listenSocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    serverSocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host, port):
        #Server Connect
        self.serverConnect(host, port)
        
        #Listen
        self.listeningThread()
        

    def listeningThread(self):
        #listenSocket
        self.listenSocket.bind((CLIENT['IP'], (int)(CLIENT['PORT']) ))
        self.listenSocket.listen(1)
        while True:
            (clientSocket, address) = self.listenSocket.accept()
            print ("Connection from", address)

            # print ("Thread Connection")
            threading.Thread(target = self.connectionThread(clientSocket, address)).start()

    def connectionThread(self, socket, address):
        self.send(socket, "Type 'exit' to end the connection.\n")
        threading.Thread(target = self.printChat(socket, address)).start()   
        # while True:
        #     text = input()
        #     # print ('You:\n', text)
        #     self.send(socket, text)     

    def sendChat(self, socket):
        while True:
            text = input()
            print ('You:\n', text)
            self.send(socket, text)
            

    def printChat(self, socket, address):
        while True:
            recvChat = self.recv(socket)
            # print(':'+recvChat+':')
            # print(recvChat.split('\n'))
            if recvChat.split('\n')[0] != 'exit\r':
                print(address, ":\n", recvChat)     
            else:
                print('Connection closed.')
                socket.close()
                break
                

    def serverConnect(self, host, port):
        self.serverSocket.connect((host, port))
        self.send(self.serverSocket, AUTHEN)
        # print("Server Status:")
        serverStatus = self.serverSocket.recv(4096).decode() #Server Status
        print('Connected server status: ', serverStatus)

        # print("Friend List:")
        friendListRecieve = self.recv(self.serverSocket) #FriendList

        print('Friend List:')
        self.friendList = []
        for friend in friendListRecieve.split('\n'):
            if friend != 'END' and friend != '':
                self.friendList.append(friend)
                print(friend)
        print()
                # print(friend.split(':')[0])

        # print("Heartbeat Threading!")
        threading.Thread(target = self.heartbeatThread).start() #Thread HeartBeat

    def heartbeatThread(self):
        while True:
            greetingMsg = "Hello " + CLIENT['USER']
            serverRcv = self.recv(self.serverSocket)
            if greetingMsg == serverRcv:
                # print(serverRcv)
                # print("Hello Server")
                self.send(self.serverSocket, "Hello Server")

    def send(self, socket, msg):
        socket.send(bytes(msg, 'utf-8'))

    def recv(self, socket):
        recv = socket.recv(4096).decode()
        return recv

client = ThreadedClient("128.199.83.36", 34260)