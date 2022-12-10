from socket import *
from threading import Thread

import pyaudio
from PyQt5.QtCore import QThread


class AudioMultiServer(QThread):  # 发送声音

    def __init__(self, openPort):
        super().__init__()
        self.openPort = openPort  # 我要开放的端口
        self.socketList = []
        # 以下是收发声音要用的变量
        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000
        self.closeSign = False
        self.p = pyaudio.PyAudio()
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)

        Thread(target=self.sendMyMessage).start()
        self.startListening()

    def startListening(self):  # 发送声音
        self.server = socket(AF_INET, SOCK_STREAM)
        ip_port = ("", self.openPort)  # 开放openport等待iptoconnect来连接
        self.server.bind(ip_port)
        self.server.listen()
        Thread(target=self.repeatGetConnection).start()

    def repeatGetConnection(self):
        try:
            while not self.closeSign:
                (self.conn, self.addr) = self.server.accept()
                self.socketList.append((self.conn, self.addr))
                Thread(target=self.receiveMessage,
                       args=(self.socketList[-1][0],)).start()
                print("Get It.")
        except OSError:
            print("You have END your server.")

    def receiveMessage(self, socket):
        try:
            while not self.closeSign:
                data = socket.recv(1024)
                self.tellMyself(data)
                self.broadcastExceptOne(data, socket)
        except OSError:
            print("This thread has been ended.")

    def broadcastAllSocket(self, message):
        for socket in self.socketList:
            socket[0].sendall(message)

    def broadcastExceptOne(self, message, socket):
        for s in self.socketList:
            if s != socket:
                s[0].sendall(message)

    def tellMyself(self, message):
        self.playing_stream.write(message)

    def sendMyMessage(self):
        while not self.closeSign:
            try:
                data = self.recording_stream.read(1024)
                self.broadcastAllSocket(data)
            except:
                pass

    def close(self):
        self.closeSign = True
        self.server.close()


if __name__ == "__main__":
    AudioMultiServer(22222)
