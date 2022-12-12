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
        self.isClose = False
        while True:
            try:
                self.port = port
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind(('', self.port))
                print("Bind successfully.")
                break
            except:
                print("Couldn't bind to that port")
                return
        self.connections = []
        threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):
        self.s.listen(100)
        try:
            while not self.isClose:
                c, addr = self.s.accept()
                self.connections.append(c)
                threading.Thread(target=self.handle_client, args=(
                    c,
                    addr,
                )).start()
        except OSError as e:
            print(e)
            print("Socket have been closed.")

    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                    print(f"#{client}\n{data}")
                except Exception as e:
                    print(e)
    def handle_client(self, c, addr):
        while 1:
            if self.isClose:
                break
            try:
                data = c.recv(2048)
                threading.Thread(target=self.broadcast, args=(c, data,)).start()

            except socket.error:
                c.close()
                break

    def close(self):
        self.isClose = True
        self.s.close()


if __name__ == "__main__":
    MultiAudioServer(31415)
