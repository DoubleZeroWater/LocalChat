# -*- coding: utf-8 -*-
# create time    : 2021-01-06 15:52
# author  : CY
# file    : voice_client.py
# modify time:
import socket
import threading
import time

import pyaudio
from PyQt5.QtCore import QThread


class MultiAudioClient(QThread):
    def __init__(self, ipToConnect, portToConnect):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isClose = False
        timestamp = 0

        while timestamp < 5:
            try:
                self.target_ip = ipToConnect
                self.target_port = portToConnect
                self.s.connect((self.target_ip, self.target_port))
                break
            except:
                print("Couldn't connect to server")
                time.sleep(1)
                timestamp += 1

        self.chunk_size = 1024  # 512
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 20000
        self.p = pyaudio.PyAudio()
        self.playing_stream = None
        self.recording_stream = None

    def receive_and_send(self):
        self.playing_stream = self.p.open(format=self.audio_format,
                                          channels=self.channels,
                                          rate=self.rate, output=True,
                                          frames_per_buffer=self.chunk_size)
        self.recording_stream = self.p.open(format=self.audio_format,
                                            channels=self.channels,
                                            rate=self.rate, input=True,
                                            frames_per_buffer=self.chunk_size)

        print("Connected to Server")

        # start threads
        threading.Thread(target=self.receive_server_data).start()
        threading.Thread(target=self.send_data_to_server).start()

    def receive_server_data(self):
        while True:
            try:
                if self.isClose:
                    break
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        while True:
            try:
                if self.isClose:
                    break
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass

    def close(self):
        self.isClose = True
        print(self.isClose)
