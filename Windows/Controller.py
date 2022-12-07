from functools import partial

from Logic.Message2 import Message2
from Logic.LocalIPGet import getIP
from Transfer_File.file_transfer import File_Transfer
from Windows.MyWindows import HelloWindow, TwoConnectWindow, MessageWindow, FileWindow, AudioWindow


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
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        self.nickName = nickName
        self.message.sendMessageSignal.connect(self.Message2Instance.sendMessages)
        self.message.videoButton.clicked.connect(partial(self.message.startVideoRequest, ipToConnect))
        self.message.FileButton.clicked.connect(self.message.startFileRequest)
        self.Message2Instance.videoDenySignal.connect(self.message.closeVideoRequest)
        self.Message2Instance.recvMessageSignal.connect(self.message.receiveMessage)
        self.Message2Instance.videoRequestSignal.connect(self.message.videoRequestCheck)
        self.Message2Instance.socketReadySignal.connect(self.socket_ok)

        self.Message2Instance.fileDenySignal.connect(self.message.closeFileRequest)
        self.Message2Instance.fileRequestSignal.connect(self.message.fileRequestCheck)
        self.message.goFileSignal.connect(self.show_file)

        self.Message2Instance.audioDenySignal.connect(self.message.closeAudioRequest)
        self.Message2Instance.audioRequestSignal.connect(self.message.audioRequestCheck)
        self.message.goAudioSignal.connect(self.show_audio)

    def socket_ok(self):
        self.message.show()
        self.twoConnect.close()

    # File Window
    def show_file(self):
        self.file = FileWindow(self.openPort, self.ipToConnect, self.portToConnect, self.nickName)
        self.file.nickname = self.nickName
        self.file.show()
        self.fileInstance=File_Transfer(self.ipToConnect, 5453, getIP(), 5453)
        self.fileInstance.receiveStartSignal.connect(self.file.receiveStart)
        self.fileInstance.receiveEndSignal.connect(self.file.receiveEnd)

    def show_audio(self):
        self.audio = AudioWindow(self.openPort, self.ipToConnect, self.portToConnect)
        self.audio.show()

