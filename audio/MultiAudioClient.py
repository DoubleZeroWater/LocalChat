# -*- coding: utf-8 -*-
# create time    : 2021-01-06 15:52
# author  : CY
# file    : voice_client.py
# modify time:
import select
import socket
import time
from threading import Thread

import pyaudio
from PyQt5.QtCore import QThread


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

    def receive_and_send(self):
        self.stream = self.p.open(format=self.audio_format,
                                  channels=self.channels,
                                  rate=self.rate, input=True, output=True,
                                  frames_per_buffer=self.chunk_size, stream_callback=callback)

        print("Connected to Server")
        self.stream.start_stream()
        while not self.isClose:
            time.sleep(0.1)

    def checkMessageArrive(self):
        while not self.isClose:
            checkEvent()

    def close(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.isClose = True
        print(self.isClose)
        if self.s:
            self.s.close()


data = None


def callback(in_data, frame_count, time_info, status):
    try:
        global data
        Thread(target=MultiAudioClient.staticSocket.send, args=(in_data,))
        temp = data
        data = None
    except socket.timeout:
        temp = None
        data = None
    return temp, pyaudio.paContinue


def checkEvent():
    global data
    r_list, w_list, e_list = select.select([MultiAudioClient.staticSocket], [MultiAudioClient.staticSocket], [], 5)
    if len(r_list) != 0:
        data = MultiAudioClient.staticSocket.recv(1024)


if __name__ == "__main__":
    s = MultiAudioClient("127.0.0.1", 31415)
    s.receive_and_send()
