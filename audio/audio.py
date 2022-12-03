from socket import *
from threading import Thread
import pyaudio
import struct
import json
import os
import sys
import time


class Audio(Thread):  # 发送声音

    def __init__(self, name, ip, openPort, ipToConnect, portToConnect):
        super().__init__()
        self.name = name  # 我的用户名
        self.ip = ip  # 我本机的ip
        self.openPort = openPort  # 我要开放的端口
        self.ipToConnect = ipToConnect  # 我要连接的ip
        self.portToConnect = portToConnect  # 我要连接的端口

        # 以下是收发声音要用的变量
        self.chunk_size = 1024  # 512
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 20000
        self.p = pyaudio.PyAudio()

    def run(self):
        Thread(target=self.server).start()
        Thread(target=self.client).start()

    def server(self):  # 发送声音
        server = socket(AF_INET, SOCK_STREAM)
        ip_port = ("", self.openPort)  # 开放openport等待iptoconnect来连接
        server.bind(ip_port)
        server.listen(60)  # 等待60s
        print("waiting for connection......\n")
        clientSock, addr = server.accept()

        recording_stream = self.p.open(format=self.audio_format,
                                       channels=self.channels,
                                       rate=self.rate, input=True,
                                       frames_per_buffer=self.chunk_size)
        print("Connected to Server")
        while True:
            try:
                data = recording_stream.read(1024)
                server.sendall(data)
            except:
                pass

    def client(self):  # 接收声音
        # 创建服务器
        client = socket(AF_INET, SOCK_STREAM)
        ip_port = (self.ipToConnect, self.portToConnect)
        client.connect(ip_port)
        print("connecting...")

        playing_stream = self.p.open(format=self.audio_format,
                                     channels=self.channels,
                                     rate=self.rate, output=True,
                                     frames_per_buffer=self.chunk_size)
        print("Connected to Server")
        while True:
            try:
                data = client.recv(1024)
                playing_stream.write(data)
            except:
                pass


if __name__ == '__main__':
    audio = Audio("132","192.168.43.20", 9808, "192.168.43.242", 9808)
    audio.run()
