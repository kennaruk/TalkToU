import socket
import sys
import threading
from authen import *

class SocketConnection:
    serverSocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, host, port):
        #Server Connect
        self.serverConnect(host, port)

    def serverConnect(self, host, port):
        self.serverSocket.connect((host, port))
        self.serverAuthen()
        self.serverStatusCheck()
        self.serverRcvFriendList()
        
        threading.Thread(target = self.heartbeat).start()

        threading.Thread(target = self.listen).start()

    def serverAuthen(self):
        self.sockSend(self.serverSocket, AUTHEN)

    def serverStatusCheck(self):
        serverConStatus = self.sockRecv(self.serverSocket).strip(' \n')
        if serverConStatus == '200 SUCCESS':
            print ('Server connected.')
        else:
            print ('Error while connecting server.')
            sys.exit(-1)
    
    def serverRcvFriendList(self):
        friendListRecv = self.sockRecv(self.serverSocket)
        self.printFriendList(friendListRecv)

    def printFriendList(self, friendList):
        print ('\nFriends list:\n')
        for friend in friendList.split('\n'):
            if friend != 'END' and friend != '':
                print(friend)
        print()

    def heartbeat(self):
        while True:
            greetingMsg = "Hello " + CLIENT['USER']
            serverRcv = self.sockRecv(self.serverSocket)
            if greetingMsg == serverRcv:
                self.sockSend(self.serverSocket, "Hello Server")
    
    def listen(self):
        listenSocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

        listenSocket.bind((CLIENT['IP'], (int)(CLIENT['PORT']) ))
        listenSocket.listen(1)
        while True:
            (connectionSocket, address) = listenSocket.accept()
            print ("Connection from", address)
            threading.Thread(target = self.connection, args = (connectionSocket, address)).start()
    
    def connection(self, sock, address):
        self.sockSend(sock, "Type 'exit' to end the connection.\n")
        sendMsgThread = threading.Thread(target = self.sendMsg, args = (sock, )).start()
        
        threading.Thread(target = self.recvMsg, args = (sock, address)).start()   

    def sendMsg(self, sock):
        while True:
            try:
                send_msg = sys.stdin.readline()
                print()
                send_msg = CLIENT['IP'] + ":\n" + send_msg
                self.sockSend(sock, send_msg)
            except BrokenPipeError:            
                return
    
    def recvMsg(self, sock, address):
        while True:
            try:
                recv_msg = self.sockRecv(sock)
                if not recv_msg:
                    sock.shutdown(socket.SHUT_WR)
                if recv_msg.split('\n')[0] != 'exit\r':
                    print(address, ":\n", recv_msg)     
                else:
                    print('Connection closed.')
                    sock.shutdown(socket.SHUT_WR)
                    break
            except UnicodeDecodeError:
                print('Connection closed.')                
                sock.shutdown(socket.SHUT_WR)
            except TypeError:
                print('Connection closed.')                
                sock.shutdown(socket.SHUT_WR)
            
    def sockSend(self, sock, msg):
        try:
            sock.send(bytes(msg, 'utf-8'))
        except BrokenPipeError:
            raise BrokenPipeError

    def sockRecv(self, sock):
        try:
            recvMsg = sock.recv(4096).decode()
            return recvMsg
        except UnicodeDecodeError:
            raise UnicodeDecodeError
        except TypeError:
            raise TypeError

#initiate application
TUSocket = SocketConnection("128.199.83.36", 34260)
