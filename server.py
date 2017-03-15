#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
from thread import *

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8824 # Arbitrary non-privileged port
users=[]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print ('Socket bind complete')

#Start listening on socket
s.listen(10)
print ('Socket now listening')

#send masseg to other users
def send(data,conn):
    data=data.replace('\n','')
    print ('Sending')
    if len(users)>=2:
        for i in range(len(users)):
            if users[i][0]==conn:
                name=users[i][1]
                break
            else:
                name='new'
        for i in range(len(users)):
            if users[i][0]<>conn:
                users[i][0].sendall(name + ': '+ data)
    elif len(users)==1 and users[0][0]==conn and data.find("/exit")==-1:
        users[0][0].sendall('You are alone \n')

#function for handling connections. This will be used to create threads
def clientthread(conn):
    #sending message to connected client
    try:
        users.index(conn)
    #ask user his name, and save to list
    except ValueError:
        conn.sendall("What is your name?")
        name = "/users"
        while name == "/users":
            name= conn.recv(1024).replace('\n','').replace('\r','')
            users.append([conn,name])
            conn.sendall("He "+name+'\r')
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #receiving from client
        data = conn.recv(1024)
        #exit from chat, and send message about exit to other users
        if data.find("/exit")>=0:
            reply='Disconnected with ' + addr[0] + ':' + str(addr[1])
            send(reply+'\n', conn)
            for i in range(0,len(users)):
                if users[i][0]==conn:
                    users.remove(users[i])
                    break
            print (reply)
            break
        #print users online
        elif data.find("/users")>=0:
            data_users='Users online:|'
            for i in range(len(users)):
                #if users[i][0]<>conn:
                data_users+=str(users[i][1])+'|'
            conn.sendall(data_users[:len(data_users)-1])
        #send message
        else:
            send(data,conn)
        if not data:
            break

    #came out of loop
    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    reply= 'Connected with ' + addr[0] + ':' + str(addr[1])
    print (reply)
    send(reply, conn)
	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))


s.close()
