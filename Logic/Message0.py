import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from PyQt5.QtCore import QThread, pyqtSignal


class Message0(QThread):  # for the host
    haveMessageSignal = pyqtSignal(str)
    closeSign = False
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
        try:
            while not self.closeSign:
                (self.conn, self.addr) = self.serverInstant.accept()
                self.socketList.append((self.conn, self.addr))
                Thread(target=self.receiveMessage,
                       args=(self.socketList[-1],)).start()
        except OSError:
            print("You have END your server.")

    def receiveMessage(self, socket):
        try:
            while not self.closeSign:
                message = socket[0].recv(1024).decode('utf-8')
                if message == ">CLIENT END":
                    self.socketList.remove(socket)
                    self.sendMyMessage(
                        f"SYSTEM {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{socket[1]}已经断开了连接")
                    break
                self.tellMyself(message)
                self.broadcastExceptOne(message, socket)
        except OSError:
            print("This thread has been ended.")

    def broadcastAllSocket(self, message):
        for socket in self.socketList:
            socket[0].send(message.encode('utf-8'))

    def broadcastExceptOne(self, message, socket):
        for s in self.socketList:
            if s != socket:
                s[0].send(message.encode('utf-8'))

    def tellMyself(self, message):
        self.haveMessageSignal.emit(message)

    def sendMyFile(self):
        self.broadcastAllSocket("FILE_SEND")
        self.tellMyself(f"{self.nickname}  {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n您已成功发送文件")

    def sendMyMessage(self, message):
        self.broadcastAllSocket(f"{self.nickname}  {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{message}")
        self.tellMyself(f"{self.nickname}  {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{message}")

    def tellAudioOK(self):
        self.broadcastAllSocket(f"SYSTEM {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n音频已经开启。")
        self.tellMyself(f"SYSTEM {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n音频已经开启。")
        self.broadcastAllSocket(">AudioOK")

    def tellAudioClose(self):
        self.broadcastAllSocket(f"SYSTEM {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n音频已经关闭。")
        self.tellMyself(f"SYSTEM {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n音频已经关闭。")
        self.broadcastAllSocket(">AudioClose")

    def close(self):
        self.broadcastAllSocket(f"SYSTEM  {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n房主已退出")
        self.broadcastAllSocket(">END")
        self.serverInstant.close()
