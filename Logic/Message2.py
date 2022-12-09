import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import strftime, sleep

from PyQt5.QtCore import QThread, pyqtSignal


class Message2(QThread):
    socketReadySignal = pyqtSignal()
    recvMessageSignal = pyqtSignal(str)
    videoRequestSignal = pyqtSignal(str)
    videoDenySignal = pyqtSignal()
    fileRequestSignal = pyqtSignal(str)
    fileDenySignal = pyqtSignal()
    audioRequestSignal = pyqtSignal(str)
    audioDenySignal = pyqtSignal()
    audioCloseMsgSignal = pyqtSignal()
    fileCloseMsgSignal = pyqtSignal()


    def __init__(self, openPort: int, ipToConnect: str, portToConnect: int, nickName: str, Queue):
        super(Message2, self).__init__()
        self.serverInstant = None
        self.clientInstant = None
        self.connect_end = None
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        self.nickName = nickName
        self.data = Queue
        self.closeSign = False

    def run(self):
        try:
            Thread(target=self.server).start()
            Thread(target=self.client).start()
        except Exception as e:
            print(e)

    def client(self):
        self.clientInstant = socket(AF_INET, SOCK_STREAM)
        while 1:
            try:
                if self.closeSign:
                    break
                self.clientInstant.connect((self.ipToConnect, self.portToConnect))
            except ConnectionRefusedError:
                sleep(2)
                print("Connect Fail.")
                continue
            else:
                break
        self.socketReadySignal.emit()

    def server(self):
        self.serverInstant = socket(AF_INET, SOCK_STREAM)
        self.serverInstant.bind(('', self.openPort))
        self.serverInstant.listen(300)
        self.conn, self.addr = self.serverInstant.accept()
        while not self.connect_end:
            recv_data = self.conn.recv(1024).decode('utf-8')
            if recv_data == "##":
                # 自身连接
                self.clientInstant.close()
                self.serverInstant.close()
                self.recvMessageSignal.emit(
                    f"SYSTEM  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n对方已经断开了连接")
                break
            elif recv_data == "VIDEO_REQUEST":
                self.videoRequestSignal.emit(self.ipToConnect)
            elif recv_data == "VIDEO_DENY":
                self.videoDenySignal.emit()
            elif recv_data == "FILE_REQUEST":
                self.fileRequestSignal.emit(self.ipToConnect)
            elif recv_data == "FILE_DENY":
                self.fileDenySignal.emit()
            elif recv_data == "AUDIO_REQUEST":
                self.audioRequestSignal.emit(self.ipToConnect)
            elif recv_data == "AUDIO_DENY":
                self.audioDenySignal.emit()
            elif recv_data == "AUDIO_CLOSE":
                self.audioCloseMsgSignal.emit(self.ipToConnect)
            elif recv_data == "FILE_CLOSE":
                self.fileCloseMsgSignal.emit()
            elif recv_data:
                self.recvMessageSignal.emit(recv_data)
                # print('\b\b\b\b{} >>: {}\t{}\n\n>>: '.format(self.receiverIP, recv_data,strftime("%Y/%m/%d %H:%M:%S", gmtime())),end="")

    def sendMessages(self, message: str):
        try:
            self.clientInstant.send(bytes(message, encoding='utf-8'))
        except:
            self.recvMessageSignal.emit(
                f"SYSTEM  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n对方无响应，请点击返回重新连接")
            self.serverInstant.close()
            self.clientInstant.close()

    def close(self):
        self.closeSign = True
        if self.serverInstant:
            self.serverInstant.close()
        if self.clientInstant:
            try:
                self.clientInstant.send(bytes("##", encoding='utf-8'))
            except OSError:
                pass
            self.clientInstant.close()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.close()
