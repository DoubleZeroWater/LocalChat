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

        # start threads
        threading.Thread(target=self.receive_server_data).start()

    def receive_server_data(self):
        try:
            self.stream.start_stream()
            while self.stream.is_active() and (not self.isClose):
                time.sleep(0.1)
                print("GAGAGAGAGGAGAG")

        except Exception as e:
            print(e)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.isClose = True
        print(self.isClose)
        self.s.close()


def callback(in_data, frame_count, time_info, status):
    MultiAudioClient.staticSocket.send(in_data)
    data = MultiAudioClient.staticSocket.recv(1024)
    return data, pyaudio.paContinue


if __name__ == "__main__":
    s = MultiAudioClient("127.0.0.1", 31415)
    s.receive_and_send()
