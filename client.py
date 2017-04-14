#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import socket
import os
import json
import sys
import re
import selectors
import time
import threading

SEL = selectors.DefaultSelector()

HOST = 'localhost'
PORT = 2101
MSIZE = 1024
FILES = []
FOLDER = None
LPORT = None
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

        FILES = os.listdir(folder)
        self.files = []
        self.fnum = 0
        for fl in FILES:
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
                'port':LPORT
            }
            self.files.append(f_dict)
        print("Local files: ")
        print(FILES)

        SEL.register(self.sock, selectors.EVENT_READ, self.connect)

    def connect(self,conn,mask):
        print('Connecting')
        self.sock.connect((HOST,PORT))
        self.say("HELLO")
        strin = self.lstn()
        if strin != 'HI':
            print("Incorrect connection starter")
            self.sock.close()
        self.share()
        SEL.modify(conn, selectors.EVENT_WRITE, self.operate)

    def share(self):
        self.say('SHARE')
        tosend = json.dumps(self.files)
        self.say(tosend)
        self.say('DONE')

    def say(self,data):
        self.sock.sendall(bytes(data,'utf-8'))

    def lstn(self):
        return str(self.sock.recv(MSIZE),'utf-8')

    def recieve(self):
        sz = 1024
        rec = []
        while sz==1024:
            data = self.sock.recv(1024)
            sz = len(data)
            print(sz)
            rec = rec.append(data)
        return data

    def disconnect(self):
        self.sock.close()

    def bye(self):
        self.say("BYE")
        self.sock.close()

    def download(self,fname,rip,rport):
        print(fname)
        print(rip)
        print(rport)
        with open(os.path.join(FOLDER,fname), 'wb') as fl:
            tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tmp.connect((rip,int(rport)))
            sz = 1024
            rec = []
            tmp.send(bytes(fname,'utf-8'))
            while sz==1024:
                data = tmp.recv(1024)
                sz = len(data)
                fl.write(data)
            fl.close()
            tmp.close()

    def operate(self,conn,mask):
        inp = None
        while inp != 'EXIT':
            inp = input("Command ('?' for help) :")#SEARCH, LIST
            if 'SEARCH' in inp:
                self.say('SEARCH')
                time.sleep(1)
                self.say(inp.replace('SEARCH ',''))
                ret = json.loads(self.lstn())
                print(ret)
            elif 'LIST' in inp:
                self.say('LIST')
                data = json.loads(self.lstn())
                for entity in data:
                    print(entity)
            elif 'DOWNLOAD' in inp:
                op = inp.split(',')
                self.download(op[1],op[2],op[3])
            elif 'EXIT' in inp:
                self.bye()
            elif '?' in inp:
                print("SEARCH (filename)  -  Search for a file in servers lists")
                print("LIST (filename) - List all the files that server has")
                print("DOWNLOAD;(filename);(ip);(port) - Download a file from given host")
                print("EXIT - to exit")

class theThread(threading.Thread):
    def run(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((ip, LPORT+1))
        print("Started serving on port ")
        print( LPORT+1)
        sock.listen(5)
        tosend = []
        while True:
            print("Waiting for connections")
            conn, _ = sock.accept()
            print("Connnected to")
            print(conn)
            fname = str(conn.recv(1024).strip(),"utf-8")
            fl = open(os.path.join(sys.argv[1],fname),'rb')
            l = fl.read(1024)
            while (l):
                conn.send(l)
                l = fl.read(1024)
            fl.close()
            conn.close()

def main(fldr):
    client = Client(folder=fldr[0])
    theThread().start()
    while True:
        evts = SEL.select()
        for key, mask in evts:
            callback = key.data
            callback(key.fileobj, mask)

if __name__ == '__main__':
    LPORT = int(sys.argv[2])
    FOLDER = sys.argv[1]
    main(sys.argv[1:])
# define path to shared folder:
#   by config file
#   by command line arguments
# search for a $filename in fmt
# request a file from peer
# finish BYE
