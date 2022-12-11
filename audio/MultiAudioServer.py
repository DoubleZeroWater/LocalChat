# -*- coding: utf-8 -*-
# create time    : 2020-12-30 15:37
# author  : CY
# file    : voice_server.py
# modify time:
import socket
import threading

from PyQt5.QtCore import QThread


class MultiAudioServer(QThread):

    def __init__(self, port):
        super().__init__()
        # self.ip = socket.gethostbyname(socket.gethostname())
        self.isClose = False
        while True:
            try:
                self.port = port
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind(('', self.port))
                break
            except:
                print("Couldn't bind to that port")
                return
        self.connections = []
        threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):
        self.s.listen(100)

        # print('Running on IP: ' + self.ip)
        # print('Running on port: ' + str(self.port))
        try:
            while True:
                if self.isClose:
                    break
                c, addr = self.s.accept()
                self.connections.append(c)
                threading.Thread(target=self.handle_client, args=(
                    c,
                    addr,
                )).start()
        except OSError:
            print("Socket have been closed.")

    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self, c, addr):
        while 1:
            if self.isClose:
                break
            try:
                data = c.recv(1024)
                threading.Thread(target=self.broadcast, args=(c, data,)).start()

            except socket.error:
                c.close()
                break

    def close(self):
        self.isClose = True
        self.s.close()


if __name__ == "__main__":
    MultiAudioServer(31415)
