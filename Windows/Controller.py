from functools import partial
from threading import Thread

from Logic.Message2 import Message2
from Windows.MyWindows import HelloWindow, TwoConnectWindow, MessageWindow


class Controller:
    def __init__(self):
        self.Message2Instance = None
        self.message = None
        self.hello = None
        self.twoConnect = None

    # Hello Window
    def show_hello(self):
        self.hello = HelloWindow()
        self.hello.goTwoConnectSignal.connect(self.show_two_connect)
        self.hello.show()

    # Two Connect Window
    def show_two_connect(self):
        self.twoConnect = TwoConnectWindow()
        self.twoConnect.fromTwoConnectToMainSignal.connect(self.back_hello)
        self.twoConnect.goMessageSignal.connect(self.show_message)
        self.hello.close()
        self.twoConnect.show()

    def back_hello(self):
        self.hello.show()
        self.twoConnect.close()

    # Message Window
    def show_message(self, openPort, ipToConnect, portToConnect, nickName, Queue):
        self.message = MessageWindow()
        self.message.nickname = nickName
        self.Message2Instance = Message2(int(openPort), ipToConnect, int(portToConnect), nickName, Queue)
        self.Message2Instance.start()

        self.Message2Instance.socketReadySignal.connect(self.socket_ok)
        self.message.sendMessageSignal.connect(self.Message2Instance.sendMessages)
        self.Message2Instance.recvMessageSignal.connect(self.message.receiveMessage)


    def socket_ok(self):
        self.message.show()
        self.twoConnect.close()
