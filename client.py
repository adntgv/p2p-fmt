#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import socket
import os
import json

#command line arguments
HOST = 'localhost'
PORT = 2101

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(('8.8.8.8',80))
ip, port = s.getsockname()
del s

class Client:
    def __init__(self, sock=None, folder='shared'):
        if sock is None:
            self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        files = os.listdir(folder)
        self.files = []
        self.fnum = 0
        for fl in files:
            self.fnum= self.fnum + 1
            fname, ext = os.path.splitext(fl)
            fl = os.path.join(folder,fl)
            size = os.path.getsize(fl)
            time = os.path.getmtime(fl)
            f_dict = {
                'id':self.fnum,
                'fname': fname,
                'ftype': ext,
                'fsize': size,
                'fmod': time,#(DD/MM/YY),
                'ip':ip,
                'port':port
            }
            self.files.append(f_dict)
        print("Local files: ")
        print(files)

    def connect(self,host,port):
        print('Connecting')
        self.sock.connect((host,port))
        self.send("HELLO")
        print('sent hello')
        din = self.recieve()
        strin = str(din,"utf-8")
        if strin != 'HI':
            print("Incorrect connection starter")
            self.disconnect()
        self.share()
        print('Shared')

    def share(self):
        self.send('SHARE')
        tosend = json.dumps(self.files)
        print(tosend)
        self.send(tosend)
        self.send('DONE')

    def send(self,data):
        self.sock.send(bytes(data,'utf-8'))

    def recieve(self):
        return self.sock.recv(1024)

    def disconnect(self):
        self.sock.disconnect()

    def operate(self):
        command = None
        while command != 'EXIT':
            command = input("Command ('?' for help) :")#SEARCH, LISt
            if 'SEARCH' in command:


    def bye(self):
        pass

client = Client(folder='shared')
client.connect(HOST,PORT)
client.operate()
client.bye()

# define path to shared folder:
#   by config file
#   by command line arguments
# search for a $songname in fmt
# request a file from peer
# finish BYE
