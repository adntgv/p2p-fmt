#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import socketserver as ss
import json


fileslist = []
class TCPHandler(ss.BaseRequestHandler):
    def handle(self):
        self.verify()
        while 1:
            strin = str(self.recieve(),"utf-8")
            if strin == 'SHARE':
                self.addPeer()
            elif strin == 'SEARCH':
                self.search()
            elif strin == 'BYE':
                self.removePeer()


    def addPeer(self):
        files = json.loads(str(self.recieve(),'utf-8'))
        print(files)
        # for x in range(count):
        #     strin = str(self.recieve(),"utf-8")
        #     fileslist.append(json.loads(strin))
        #print(fileslist)

    def verify(self):
        strin = str(self.recieve(),"utf-8")
        if(strin != "HELLO"):
            print("Incorrect connection starter")
            self.sock.close()
        self.send(bytes("HI","utf-8"))

    def recieve(self):
        return self.request.recv(1024).strip()

    def send(self,data):
        return self.request.sendall(data)



if __name__ == "__main__":
    HOST, PORT = "localhost", 2101
    server = ss.TCPServer((HOST,PORT),TCPHandler)
    print("serving at port:" ,PORT)
    server.serve_forever()
