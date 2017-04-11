#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import socket
import json
import re
import selectors

sel = selectors.DefaultSelector()

fileslist = []

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, verify)

def main_loop(conn, mask):
    print('In main loop')
    strin = str(conn.recv(1024).strip(),"utf-8")
    print('STRIN : '+strin)
    if 'SHARE' in strin:
        sel.modify(conn, selectors.EVENT_READ, addPeer)
    elif 'SEARCH' in strin:
        sel.modify(conn, selectors.EVENT_READ, search)
    elif 'BYE' in strin:
        sel.modify(conn, selectors.EVENT_READ, removePeer)
    elif 'HELLO' in strin:
        conn.send(bytes("HI","utf-8"))
    else:
        pass

def addPeer(conn,mask):
    chunks = ""
    chunk = ""
    while not 'DONE' in chunk:
        chunk = str(conn.recv(1024).strip(),'utf-8')
        chunks = chunks+chunk
        chunks = re.sub(re.escape('DONE'), '', chunks)
    lst = json.loads(chunks)
    for fl in lst:
        fileslist.append(fl)
    print(fileslist)
    sel.modify(conn, selectors.EVENT_READ, main_loop)

def search(conn,mask):
    
    sel.modify(conn, selectors.EVENT_READ, main_loop)

def verify(conn,mask):
    strin = str(conn.recv(1024).strip(),"utf-8")

    if(strin != "HELLO"):
        print("Incorrect connection starter")
        sel.unregister(conn)
        conn.close()
    else:
        print('verify STRIN : '+strin)
        conn.send(bytes("HI","utf-8"))
        sel.modify(conn, selectors.EVENT_READ, main_loop)


sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost', 2101))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
