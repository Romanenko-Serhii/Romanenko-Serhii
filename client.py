#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
import threading
from threading import Thread

sock=socket.socket()
sock.connect(('localhost',8808))
def read():
	while True:
		try:
			data=str(sock.recv(1024).decode())
			if data.find("/exit")>=0:
				sock.close()
				sys.exit()
				break
			else:
				print (data)
		except socket.error:
			break
def send():
	while True:
		data=sys.stdin.readline()
		sock.send(data.encode())
		if data.find("/exit")>=0:
			sock.close()
			sys.exit()
			#pool.terminate()
			break


Thread(target = read).start()
Thread(target = send).start()
