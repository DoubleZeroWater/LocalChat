from socket import *
from threading import Thread

import pyaudio


class AudioServer(Thread):  # 发送声音

    def __init__(self, openPort, ipToConnect, portToConnect):
        super().__init__()
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect

    def run(self):
        Thread(target=self.server).start()

    def server(self):
        server = socket(AF_INET, SOCK_STREAM)
        ip_port = (self.ipToConnect, self.openPort)
        server.bind(ip_port)
        server.listen(60)
        print("waiting for connectiom......\n")
        clientSock, addr = server.accept()

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        p = pyaudio.PyAudio()
        recording_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                  frames_per_buffer=chunk_size)
        print("Connected to Server")
        while True:
            try:
                data = recording_stream.read(1024)
                server.sendall(data)
            except:
                pass


class AudioClient(Thread):  # 接收声音
    def __init__(self, name, ip, openPort, ipToConnect, portToConnect):
        super().__init__()
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        self.name = name
        self.ip = ip

    def run(self):
        Thread(target=self.client).start()

    def client(self):
        # 创建服务器
        client = socket(AF_INET, SOCK_STREAM)
        ip_port = (self.ip, self.openPort)  #############
        client.connect(ip_port)
        print("connecting...")

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        p = pyaudio.PyAudio()
        playing_stream = p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                frames_per_buffer=chunk_size)
        print("Connected to Server")
        while True:
            try:
                data = client.recv(1024)
                playing_stream.write(data)
            except:
                pass


if __name__ == '__main__':
    server = AudioServer(12345, "192.168.43.242", 12345)
    server.run()
    client = AudioServer("132", "192.168.43.20", 12345, "192.168.43.242", 12345)
    client.run()
