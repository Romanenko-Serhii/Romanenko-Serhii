#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit,
     QGridLayout, QApplication)
from PyQt5.QtCore import *#(Qt, QThread, QThreadPool, pyqtSignal)

import socket
import threading
from threading import Thread

class Example(QWidget):
    mySignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()
        self.sock=socket.socket()
        self.sock.connect(('localhost',8813))
        self.workerThread = Read(self.sock)
        self.workerThread.mySignal.connect(self.test)
        self.workerThread.start()
        self.chat_data = ''
    def initUI(self):

        self.chat = QLabel(self)
        self.chat.setStyleSheet("QWidget { background-color: white }")
        self.chat.setAlignment(Qt.AlignLeft)

        self.user = QLabel(self)
        self.user.setStyleSheet("QWidget { background-color: white }")
        self.user.setAlignment(Qt.AlignLeft)

        self.textSend = QLineEdit()
        self.sendButton = QPushButton("Send")
        self.sendButton.clicked.connect(self.on_click)

        grid = QGridLayout()
        grid.setSpacing(20)

        grid.addWidget(self.chat, 1, 0, 5, 3)
        grid.addWidget(self.user, 1, 3, 4, 1)

        grid.addWidget(self.textSend, 6, 0,1,3)
        grid.addWidget(self.sendButton, 6, 3,1,1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 700, 600)
        self.setWindowTitle('Review')
        self.show()

    def test(self,text):
        self.chat_data = self.chat_data +text+'\n'
        self.chat.setText(self.chat_data)
        self.textSend.clear()

    @pyqtSlot()
    def on_click(self):
        data = self.textSend.text()
        self.test('You: ' + data)
        self.sock.send(data.encode())
        if data.find("/exit")>=0:
            self.sock.close()
            sys.exit(app.exec_())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Enter:
            self.on_click()

class Read(QThread):
    mySignal = pyqtSignal(str)

    def __init__(self, sock):
        super().__init__()
        self.sock = sock
    def run(self):
        while True:
            try:
                data=str(self.sock.recv(1024).decode())
                if data.find("/exit")>=0:
                    self.sock.close()
                    sys.exit()
                    break
                else:
                    print (data)
                    self.mySignal.emit(data)

            except socket.error:
                break

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    sock.close()
