#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import json
import re
import socket

import selectors

SEL = selectors.DefaultSelector()

FILELIST = []

def accept(l_sock,mask):
    """Accept connections and send to verify."""
    conn, _ = l_sock.accept()  # Should be ready
    print('accepted', conn)
    conn.setblocking(False)
    SEL.register(conn, selectors.EVENT_READ, verify)

def main_loop(conn,mask):
    """Main loop routes actions."""
    print('In main loop')
    strin = str(conn.recv(1024).strip(), "utf-8")
    print('STRIN : '+strin)
    if 'SHARE' in strin:
        SEL.modify(conn, selectors.EVENT_READ, addPeer)
    elif 'SEARCH' in strin:
        SEL.modify(conn, selectors.EVENT_READ, search)
    elif 'LIST' in strin:
        lst(conn,mask)
    elif 'BYE' in strin:
        for fl in FILELIST:
            if fl[ip]==conn[ip]:
                FILELIST.remove(fl)
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
        FILELIST.append(fl)
    print(FILELIST)
    SEL.modify(conn, selectors.EVENT_READ, main_loop)

def search(conn,mask):
    strin = str(conn.recv(1024).strip(), "utf-8")
    tosend = []
    print("Searching for " + strin)
    for filedesc in FILELIST:
        for field in filedesc:
            print(field)
            if strin == filedesc[field]:
                tosend.append(filedesc)
                print("Found " + field)
    if len(tosend) == 0 :
        conn.send(bytes(json.dumps("NOT FOUND"),"utf-8"))
    else:
        conn.send(bytes(json.dumps(tosend),"utf-8"))
    SEL.modify(conn, selectors.EVENT_READ, main_loop)

def lst(conn,mask):
    print("in list")
    conn.send(bytes(json.dumps(FILELIST),"utf-8"))
    print("listed")
    SEL.modify(conn, selectors.EVENT_READ, main_loop)


def verify(conn,mask):
    strin = str(conn.recv(1024).strip(),"utf-8")

    if(strin != "HELLO"):
        print("Incorrect connection starter")
        SEL.unregister(conn)
        conn.close()
    else:
        print('verify STRIN : '+strin)
        conn.send(bytes("HI","utf-8"))
        SEL.modify(conn, selectors.EVENT_READ, main_loop)

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost', 2101))
sock.listen(100)
sock.setblocking(False)
SEL.register(sock, selectors.EVENT_READ, accept)

while True:
    evts = SEL.select()
    for key, mask in evts:
        callback = key.data
        callback(key.fileobj, mask)
