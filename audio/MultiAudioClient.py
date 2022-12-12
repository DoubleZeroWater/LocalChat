# -*- coding: utf-8 -*-
# create time    : 2021-01-06 15:52
# author  : CY
# file    : voice_client.py
# modify time:
import socket
import time
from threading import Thread

import pyaudio
from PyQt5.QtCore import QThread

data = None
i = 0


class MultiAudioClient(QThread):
    staticSocket = None

    def __init__(self, ipToConnect, portToConnect):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        MultiAudioClient.staticSocket = self.s
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

        if timestamp == 5:
            print("Bad connection.")

    def receive_and_send(self):
        self.stream = self.p.open(format=self.audio_format,
                                  channels=self.channels,
                                  rate=self.rate, input=True, output=True,
                                  frames_per_buffer=self.chunk_size, stream_callback=callback)
        Thread(target=self.checkMessageArrive).start()
        print("Connected to Server")
        self.stream.start_stream()
        while not self.isClose:
            # print("Main is running.")
            time.sleep(0.1)

    def checkMessageArrive(self):
        while not self.isClose:
            global data
            data = self.s.recv(2048)

    def close(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.isClose = True
        print(self.isClose)
        if self.s:
            self.s.close()


def callback(in_data, frame_count, time_info, status):
    try:
        global data
        global i
        # print(len(in_data))
        MultiAudioClient.staticSocket.send(in_data)
        if data is None:
            data = None
            # print(f"#{i} Recevice None")
            return b"\x00" * 2048, pyaudio.paContinue
        else:
            temp = data
            # print(f"#{i} Recevice \n{data}")
            data = None
            print(f"#Haha\n{temp}")
            return temp, pyaudio.paContinue
    except socket.timeout:
        return None, pyaudio.paComplete


if __name__ == "__main__":
    s = MultiAudioClient("127.0.0.1", 31415)
    s.receive_and_send()
