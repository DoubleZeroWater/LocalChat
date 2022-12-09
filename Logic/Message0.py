import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from PyQt5.QtCore import QThread, pyqtSignal


class Message0(QThread):  # for the host
    haveMessageSignal = pyqtSignal(str)

    def __init__(self, openPort: int, nickname: str):
        self.socketList = []
        self.openPort = openPort
        self.nickname = nickname
        super(Message0, self).__init__()
        Thread(target=self.startListening).start()

    def startListening(self):
        self.serverInstant = socket(AF_INET, SOCK_STREAM)
        self.serverInstant.bind(('', self.openPort))
        self.serverInstant.listen()
        self.acceptConnection()

    def acceptConnection(self):
        Thread(target=self.repeatGetConnection).start()

    def repeatGetConnection(self):
        while True:
            (self.conn, self.addr) = self.serverInstant.accept()
            self.socketList.append((self.conn, self.addr))
            Thread(target=self.receiveMessage,
                   args=(self.socketList[-1],)).start()

    def receiveMessage(self, socket):
        while True:
            message = socket[0].recv(1024).decode('utf-8')
            self.tellMyself(message)
            self.broadcastExceptOne(message, socket)

    def broadcastAllSocket(self, message):
        for socket in self.socketList:
            socket[0].send(message.encode('utf-8'))

    def broadcastExceptOne(self, message, socket):
        for s in self.socketList:
            if s != socket:
                s[0].send(message.encode('utf-8'))

    def tellMyself(self, message):
        self.haveMessageSignal.emit(message)

    def sendMyMessage(self, message):
        self.broadcastAllSocket(f"{self.nickname}@{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>{message}")
        self.tellMyself(f"{self.nickname}@{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>{message}")
