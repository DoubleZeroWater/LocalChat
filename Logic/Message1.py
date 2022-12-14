import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import strftime

from PyQt5.QtCore import QThread, pyqtSignal


class Message1(QThread):  # for the host
    socketReadySignal = pyqtSignal()
    haveMessageSignal = pyqtSignal(str)
    audioSignal = pyqtSignal(str)
    audioCloseSignal = pyqtSignal()
    haveMultiFileSignal = pyqtSignal()
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
                self.haveMessageSignal.emit(
                    f"SYSTEM  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{self.nickname} 加入了聊天室")
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
                elif message == "FILE_SEND":
                    self.haveMultiFileSignal.emit()
                    self.haveMessageSignal.emit(
                        f"SYSTEM {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n你将要接受一个文件。")
                else:
                    self.haveMessageSignal.emit(message)
        except OSError:
            print("You have successfully disconnected from server.")

    def receive(self):
        Thread(target=self.repeatReceive).start()

    def sendMyMessage(self, message):
        self.haveMessageSignal.emit(f"{self.nickname}  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{message}")
        self.send(f"{self.nickname}  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{message}")

    def acceptAudio(self):
        self.send(f"SYSTEM  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{self.nickname}已经加入了语音。")
        self.haveMessageSignal.emit(
            f"SYSTEM  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{self.nickname}已经加入了语音。")

    def closeAudio(self):
        self.send(f"SYSTEM  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{self.nickname}已经退出了语音。")
        self.haveMessageSignal.emit(
            f"SYSTEM  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{self.nickname}已经退出了语音。")

    def close(self):
        self.send(">CLIENT END")
        self.closeSign = True
        self.client.close()
