#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import socket
import os
import json

#command line arguments
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

    def connect(self,host,port):
        self.sock.connect((host,port))
        self.sock.send(bytes("HELLO","utf-8"))
        din = self.recieve()
        strin = str(din,"utf-8")
        if strin != 'HI':
            print("Incorrect connection starter")
            self.sock.disconnect()
        self.share()

    def share(self):
        self.send(bytes('SHARE',"utf-8"))
        self.send(bytes(json.dumps(self.files),"utf-8"))
        self.send(bytes('DONE',"utf-8"))

    def send(self,data):
        self.sock.send(data)

    def recieve(self):
        return self.sock.recv(1024)

    def disconnect(self):
        self.sock.disconnect()

    def operate(self):
        pass

    def bye(self):
        pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 2101
    client = Client(folder='shared')
    client.connect(HOST,PORT)
    client.operate()
    client.bye()

# define path to shared folder:
#   by config file
#   by command line arguments
# send list to server
# search for a $songname in fmt
# request a file from peer
# finish BYE
