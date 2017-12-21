from tkinter import *
from tusocket import *
from tkinter import *
from tkinter import messagebox
import socket
import sys
import threading

class HomePageGUI(Frame):
    def __init__(self, master):
        self.serverSocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

        self.master = master
        master.title("TalkToU")

        self.label = Label(master, text="Talk To U")
        self.label.grid(row=1, columnspan=2, sticky=N+E+W+S)
        
        self.usernameLbl = Label(master, text="Username: ")
        self.usernameLbl.grid(row=2)

        self.usernameEnt = Entry(master)
        self.usernameEnt.grid(row=2, column=1)

        self.passwordLbl = Label(master, text="Password: ")
        self.passwordLbl.grid(row=3)

        self.passwordEnt = Entry(master)
        self.passwordEnt.grid(row=3, column=1)

        self.ipLbl = Label(master, text="IP: ")
        self.ipLbl.grid(row = 4)
        
        ip = StringVar(master, value=socket.gethostbyname(socket.gethostname()))
        self.ipEnt = Entry(master, textvariable=ip, state='disable')
        self.ipEnt.grid(row=4, column=1)

        self.portLbl = Label(master, text="PORT: ")
        self.portLbl.grid(row = 5)
        
        self.portEnt = Entry(master)
        self.portEnt.grid(row=5, column=1)

        self.loginBtn = Button(master, text="Login", command=self.login)
        self.loginBtn.grid(row=6, columnspan=2, sticky=N+W+S+E)

    def login(self):
        self.user = {
            'USER': self.usernameEnt.get(),
            'PASS': self.passwordEnt.get(),
            'IP': socket.gethostbyname(socket.gethostname()),
            'PORT': self.portEnt.get()
        }
        AUTHEN = "USER:" + self.user['USER'] + "\n" + \
                "PASS:" + self.user['PASS'] + "\n" + \
                "IP:" + self.user['IP'] + "\n" + \
                "PORT:" + self.user['PORT'] + "\n"

        self.serverSocket.connect(('128.199.83.36', 34260))
        self.sockSend(self.serverSocket, AUTHEN)
        serverConStatus = self.sockRecv(self.serverSocket).strip(' \n')

        if serverConStatus == '200 SUCCESS':
            friendListRcv = self.sockRecv(self.serverSocket)
            friendList = []
            for friend in friendListRcv.split('\n'):
                if friend != 'END' and friend != '':
                    friendList.append(friend)

            payload = {
                'user': self.user,
                'friendList': friendList
            }
            threading.Thread(target = self.heartbeat).start()
            messagebox.showinfo('Connect success', 'Enjoy your chat!')
            self.master.withdraw()
            listPageGui = ListPageGUI(payload)            
        else:
            messagebox.showinfo('Error while connecting server.', 'Please try again.')
    
    def heartbeat(self):
        while True:
            greetingMsg = "Hello " + self.user['USER']
            serverRcv = self.sockRecv(self.serverSocket)
            if greetingMsg == serverRcv:
                self.sockSend(self.serverSocket, "Hello Server")
    

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

class ListPageGUI(Toplevel):
    def __init__(self, payload):
        # self.title("TalkToU")
        Toplevel.__init__(self)
        headerText = payload['user']['USER'] + " " + payload['user']['IP'] + " " + payload['user']['PORT']
        Label(self, text=headerText).pack()

        ''' frame1 '''
        frame = Frame(self)       
        frame.pack()
        scroll = Scrollbar(frame, orient=VERTICAL)
      
        self.select = Listbox(frame, yscrollcommand=scroll.set, height=6, width=30)
        self.select.bind('<<ListboxSelect>>', self.onselect)
        for i in range(len(payload['friendList'])):
            self.select.insert(END, payload['friendList'][i])
        scroll.config (command=self.select.yview)
        scroll.pack(side=RIGHT, fill=Y)

        self.select.pack(side=LEFT,  fill=BOTH, expand=1)

        ''' frame2 '''
        frame2 = Frame(self)
        frame2.pack()
        ipLbl = Label(frame2, text="      IP: ")
        ipLbl.pack(side=LEFT)
        
        self.ipEnt = Entry(frame2)
        self.ipEnt.pack(side=RIGHT)

        ''' frame3'''
        frame3 = Frame(self)
        frame3.pack()
        portLbl = Label(frame3, text="PORT: ")
        portLbl.pack(side=LEFT)
        
        self.portEnt = Entry(frame3)
        self.portEnt.pack(side=RIGHT)

        '''End Frame'''
        startChatBtn = Button(self, text="Start Chat", command=self.startChat)
        startChatBtn.pack(fill=X)
    
    def startChat(self):
        print(self.select.get(ACTIVE))
    
    def onselect(self, evt):
        selectRow = self.select.get(ACTIVE)
        ip = StringVar(self, selectRow.split(':')[1])
        self.ipEnt.config(textvariable=ip)

        port = StringVar(self, selectRow.split(':')[2])
        self.portEnt.config(textvariable=port)


root = Tk()
root.attributes("-topmost", True)
home_gui = HomePageGUI(root)
root.mainloop()