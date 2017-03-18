#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, time
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit,
     QGridLayout, QApplication, QInputDialog, QScrollArea)
from PyQt5.QtCore import (Qt, QThread, QThreadPool, pyqtSignal, pyqtSlot)

import socket

class Example(QWidget):
    mySignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()
        self.sock=socket.socket()
        self.sock.connect(('localhost',8873))
        self.workerThread = Read(self.sock)
        self.workerThread.mySignal.connect(self.logics)
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
        self.setWindowTitle('TCP Chat')
        self.show()

    def logics(self, text):
        if text.find("Users online")>=0:
            user_online=''
            for user in text.split("|"):
                user_online += user+"\n"
            self.user.setText(user_online)
        elif text.find("What is your name?")>=0:
            self.showLogin()
        else:
            self.write_to_chat(text)

    def write_to_chat(self, text):
        self.chat_data = self.chat_data +text+'\n'
        self.chat.setText(self.chat_data)


    @pyqtSlot()
    def on_click(self):
        data = self.textSend.text()
        self.textSend.clear()
        self.logics('You: ' + data)
        self.sock.send(data.encode())
        if data.find("/exit")>=0:
            self.sock.close()
            sys.exit(app.exec_())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Return:
            self.on_click()

    def showLogin(self):

        text, ok = QInputDialog.getText (self, 'Login', 'Enter your name:')
        if ok:
            self.sock.send(text.encode())

    def closeEvent(self, event):
        data = "/exit"
        self.sock.send(data.encode())
        self.sock.close()
        sys.exit()
        event.accept()

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
#not required
class CheckUsersOnline(QThread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def run(self):
        while True:
            time.sleep(5)
            data = "/users"
            self.sock.send(data.encode())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())