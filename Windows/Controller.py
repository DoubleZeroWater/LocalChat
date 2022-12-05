from functools import partial
from threading import Thread

from Logic.Message2 import Message2
from Logic.Message3 import Message3
from Windows.MyWindows import HelloWindow, TwoConnectWindow, MessageWindow,FileWindow


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

        self.message.sendMessageSignal.connect(self.Message2Instance.sendMessages)
        self.message.videoButton.clicked.connect(partial(self.message.startVideoRequest, ipToConnect))
        self.Message2Instance.videoDenySignal.connect(self.message.closeVideoRequest)
        self.Message2Instance.recvMessageSignal.connect(self.message.receiveMessage)
        self.Message2Instance.videoRequestSignal.connect(self.message.videoRequestCheck)
        self.Message2Instance.socketReadySignal.connect(self.socket_ok)

        self.message.goFileSignal.connect(partial(self.show_file, openPort, ipToConnect, portToConnect, self.message.nickname))

        self.Message2Instance.fileDenySignal.connect(self.message.closeFileRequest)
        self.Message2Instance.fileRequestSignal.connect(self.message.fileRequestCheck)




    def socket_ok(self):
        self.message.show()
        self.twoConnect.close()


   # File Window
    def show_file(self, openPort, ipToConnect, portToConnect, nickName):
        self.file = FileWindow(openPort, ipToConnect, portToConnect, nickName)
        self.file.nickname = nickName
        self.file.show()
