# -*- coding: utf-8 -*-
# create time    : 2021-01-06 15:52
# author  : CY
# file    : voice_client.py
# modify time:
import socket
import threading

import pyaudio
from PyQt5.QtCore import QThread


class AudioMultiClient(QThread):
    def __init__(self, ipToConnect, portToConnect):
        super().__init__()
        chunk_size = 4096  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000
        self.CloseSign = False
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        threading.Thread(target=self.startConnecting).start()

    def startConnecting(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ipToConnect, self.portToConnect))
        threading.Thread(target=self.receiveServerData).start()
        threading.Thread(target=self.sendDataToServer).start()

    def receiveServerData(self):
        while not self.CloseSign:
            try:
                data = self.client.recv(4096)
                self.playing_stream.write(data)
            except:
                pass

    def sendDataToServer(self):
        while not self.CloseSign:
            try:
                data = self.recording_stream.read(4096)
                self.client.send(data)
            except:
                pass

    def close(self):
        self.CloseSign = True
        self.client.close()


if __name__ == "__main__":
    AudioMultiClient("127.0.0.1", 22222)
