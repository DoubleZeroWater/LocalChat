from functools import partial
from threading import Thread

from Logic.Message2 import Message2
from Windows.MyWindows import HelloWindow, TwoConnectWindow, MessageWindow


class Controller:
    def __init__(self):
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
        MessageThread = Thread(target=Message2(int(openPort), ipToConnect, int(portToConnect), nickName, Queue).go)
        MessageThread.start()
        if Queue.get(False) == "Connected":
            self.message = MessageWindow()
            self.message.show()
            self.twoConnect.close()
        else:
            self.twoConnect.label_4.hide()
            MessageThread.join()



