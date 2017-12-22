from tkinter import *
from tkinter import *
from tkinter import messagebox
import socket
import sys
import threading
payload = "DUMMYID:IP:PORT"
friendLists = [
    "5809610115:-1:-1",
    "5709035116:-1:-1",
    "5809520025:192.168.43.120:53000",
    "5809610248:172.25.80.184:12345",
    "5809610040:192.168.43.120:75555",
    "5809610321:192.168.43.15:34261",
    "5809610255:192.168.43.28:30000",
    "5809650756:192.168.1.8:23"
]

class ChatPageGUI:
    def __init__(self, master):
        self.screenWidth = 50
        self.master = master
        master.title("TalkToU")

        Label(master, text="[Taling to] 192.168.1.1 95" ).pack()

        ''' Text chat frame '''
        frame = Frame(master)       
        frame.pack()
      
        scroll = Scrollbar(frame, orient=VERTICAL)        
        scroll.pack(side=RIGHT, fill=Y, expand=True)
      
        self.textArea = Text(frame, height=20, width=self.screenWidth)
        self.textArea.pack(side=LEFT,  fill=BOTH, expand=True)
        self.textArea.tag_configure('recieve', justify='left')
        self.textArea.tag_configure('send', justify='right')
        
        self.textArea.tag_add('recieve', 1.0, 'end')
        self.textArea.tag_add('send', 2.0, 'end')

        for i in range (10):
            self.textArea.insert('end', 'senddd\n', ('send'))
            self.textArea.insert('end', 'recvvv\n', ('recieve'))
        self.textArea.config(state=DISABLED)

        scroll.config(command=self.textArea.yview)
        self.textArea.config(yscrollcommand=scroll.set)      
        
        ''' Enter message and send frame '''
        frame2 = Frame(master)
        frame2.pack(side=LEFT)
        messageLbl = Label(frame2, text="Message: ")
        messageLbl.pack(side=LEFT)
        
        sendBtn = Button(frame2, text="SEND", command=self.sendMessage)
        sendBtn.pack(side=RIGHT)

        self.messageEnt = Entry(frame2, width=self.screenWidth)
        self.messageEnt.pack(side=LEFT)
        
        self.master.bind('<Return>', self.sendMessage)

    def sendMessage(self, event=None):
        msg = self.messageEnt.get()
        if msg != "":
            self.messageEnt.delete(0, 'end')
            self.textArea.config(state=NORMAL)
            self.textArea.insert('end', msg+'\n', ('send'))
            self.textArea.config(state=DISABLED)
            self.textArea.see(END)

root = Tk()
root.attributes("-topmost", True)
chat_gui = ChatPageGUI(root)
root.mainloop()

