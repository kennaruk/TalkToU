from tkinter import *
from tusocket import *
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

class ListPageGUI:
    def __init__(self, master):
        self.master = master
        master.title("TalkToU")

        Label(master, text=payload).pack()

        ''' frame1 '''
        frame = Frame(master)       
        frame.pack()
        scroll = Scrollbar(frame, orient=VERTICAL)
      
        self.select = Listbox(frame, yscrollcommand=scroll.set, height=6, width=30)
        self.select.bind('<<ListboxSelect>>', self.onselect)
        for i in range(len(friendLists)):
            self.select.insert(END, friendLists[i])
        scroll.config (command=self.select.yview)
        scroll.pack(side=RIGHT, fill=Y, expand=True)

        self.select.pack(side=LEFT,  fill=BOTH, expand=True)

        ''' frame2 '''
        frame2 = Frame(master)
        frame2.pack()
        ipLbl = Label(frame2, text="      IP: ")
        ipLbl.pack(side=LEFT)
        
        self.ipEnt = Entry(frame2)
        self.ipEnt.pack(side=RIGHT)

        ''' frame3'''
        frame3 = Frame(master)
        frame3.pack()
        portLbl = Label(frame3, text="PORT: ")
        portLbl.pack(side=LEFT)
        
        self.portEnt = Entry(frame3)
        self.portEnt.pack(side=RIGHT)

        '''End Frame'''
        startChatBtn = Button(master, text="Start Chat", command=self.startChat)
        startChatBtn.pack(fill=X)
    
    def startChat(self):
        print(self.select.get(ACTIVE))
    
    def onselect(self, evt):
        selectRow = self.select.get(ACTIVE)
        ip = StringVar(self.master, selectRow.split(':')[1])
        self.ipEnt.config(textvariable=ip)

        port = StringVar(self.master, selectRow.split(':')[2])
        self.portEnt.config(textvariable=port)

root = Tk()
root.attributes("-topmost", True)
home_gui = ListPageGUI(root)
root.mainloop()

