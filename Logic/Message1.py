import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import strftime

from PyQt5.QtCore import QThread, pyqtSignal


class Message1(QThread):  # for the host
    socketReadySignal = pyqtSignal()
    haveMessageSignal = pyqtSignal(str)
    audioSignal = pyqtSignal()
    audioCloseSignal = pyqtSignal()
    closeSign = False

    def __init__(self, ip, port, nickname):
        super(Message1, self).__init__()
        self.ip = ip
        self.port = port
        self.nickname = nickname
        Thread(target=self.connect).start()

    def connect(self):
        times = 5
        while times:
            try:
                self.client = socket(AF_INET, SOCK_STREAM)
                ipPort = (self.ip, self.port)
                self.client.connect(ipPort)
                self.send(f"SYSTEM  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{self.nickname} 加入了聊天室")
                self.receive()
                break
            except ConnectionRefusedError:
                times = times - 1
                time.sleep(2)
            except OSError:
                print("Socket has been closed.")
                break
            except:
                break

    def send(self, message):
        try:
            self.client.send(message.encode('utf-8'))
        except OSError:
            self.haveMessageSignal.emit(
                f"SYSTEM {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n你的连接已经断开。")

    def repeatReceive(self):
        try:
            while not self.closeSign:
                message = self.client.recv(1024).decode('utf-8')
                if message == ">END":
                    self.close()
                    self.haveMessageSignal.emit(
                        f"SYSTEM {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n远程主机已经断开了与你的连接，请返回。")
                    break
                elif message == ">AudioOK":
                    self.audioSignal.emit(self.ip)
                elif message == ">AudioClose":
                    self.audioCloseSignal.emit()
                self.haveMessageSignal.emit(message)
        except OSError:
            print("You have successfully disconnected from server.")

    def receive(self):
        Thread(target=self.repeatReceive).start()

    def sendMyMessage(self, message):
        self.send(f"{self.nickname}  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{message}")
        self.haveMessageSignal.emit(f"{self.nickname}  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{message}")

    def sendMyFile(self, message):
        self.send(f"{self.nickname}  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{'对方已发送文件，接受中...'}")
        self.haveMessageSignal.emit(f"{self.nickname}  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{'你已成功发送文件'}")

    def close(self):
        self.send(">CLIENT END")
        self.closeSign = True
        self.client.close()
