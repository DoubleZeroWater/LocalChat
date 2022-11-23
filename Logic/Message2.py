import sys
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import strftime, gmtime, sleep

from PyQt5.QtCore import QThread, pyqtSignal


class Message2(QThread):
    socketReadySignal = pyqtSignal()
    recvMessageSignal = pyqtSignal(str)

    def __init__(self, openPort: int, ipToConnect: str, portToConnect: int, nickName: str, Queue):
        super(Message2, self).__init__()
        self.serverInstant = None
        self.clientInstant = None
        self.connect_end = None
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        self.nickName = nickName
        self.data = Queue


    def run(self):
        Thread(target=self.server).start()
        Thread(target=self.client).start()

    def client(self):
        self.clientInstant = socket(AF_INET, SOCK_STREAM)
        while 1:
            try:
                self.clientInstant.connect((self.ipToConnect, self.portToConnect))
            except ConnectionRefusedError:
                sleep(2)
                print("Connect Fail.")
                continue
            else:
                break
        self.socketReadySignal.emit()

    def server(self):
        self.serverInstant = socket(AF_INET, SOCK_STREAM)
        self.serverInstant.bind(('', self.openPort))
        self.serverInstant.listen(60)
        self.conn, self.addr = self.serverInstant.accept()
        while not self.connect_end:
            recv_data = self.conn.recv(1024).decode('utf-8')
            if recv_data == "##":
                # 自身连接
                self.clientInstant.close()
                self.serverInstant.close()
                self.connect_end = True
                print('\n---> 与 {} 断开的连接已中断... '.format(self.addr))
                sys.exit(0)
                break
            elif recv_data:
                self.recvMessageSignal.emit(recv_data)
                #print('\b\b\b\b{} >>: {}\t{}\n\n>>: '.format(self.receiverIP, recv_data,strftime("%Y/%m/%d %H:%M:%S", gmtime())),end="")
    def sendMessages(self, message: str):
        try:
            self.clientInstant.send(bytes(message, encoding='utf-8'))
            if message == '##':
                self.clientInstant.close()
                self.serverInstant.close()
                self.connect_end = True
                sys.exit(0)
        except:
            print('---> 服务已断开...')
            self.serverInstant.close()
