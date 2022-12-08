import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import strftime

from PyQt5.QtCore import QThread, pyqtSignal


class Message1(QThread):  # for the host
    socketReadySignal = pyqtSignal()
    haveMessageSignal = pyqtSignal(str)

    def __init__(self, ip, port, nickname):
        super(Message1, self).__init__()
        self.ip = ip
        self.port = port
        self.nickname = nickname
        Thread(target=self.connect).start()

    def connect(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        ipPort = (self.ip, self.port)
        self.client.connect(ipPort)
        self.receive()

    def send(self, message):
        self.client.send(message.encode('utf-8'))

    def repeatReceive(self):
        while True:
            message = self.client.recv(1024).decode('utf-8')
            self.haveMessageSignal.emit(message)

    def receive(self):
        Thread(target=self.repeatReceive).start()

    def sendMyMessage(self, message):
        self.send(f"{self.nickname}@{strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>{message}")
        self.haveMessageSignal.emit(f"{self.nickname}@{strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>{message}")
