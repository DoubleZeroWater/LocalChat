from functools import partial

from Logic.Message0 import Message0
from Logic.Message1 import Message1
from Logic.Message2 import Message2
from Transfer_File.file_transfer import transfer
from Transfer_File1.file_transfer1 import transfer1
from File_multiple.client import Client
from File_multiple.server import Server
from Windows.MyWindows import HelloWindow, TwoConnectWindow, MessageWindow, FileWindow, AudioWindow, MultiHostWindow, \
    MultiMessageWindow, MultiClientWindow


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
        self.hello.goMultiConnectSignalHost.connect(self.show_multi_host)
        self.hello.goMultiConnectSignalClient.connect(self.show_multi_client)
        self.hello.show()

    # Two Connect Window
    def show_two_connect(self):
        self.twoConnect = TwoConnectWindow()
        self.twoConnect.fromTwoConnectToMainSignal.connect(self.back_hello)
        self.twoConnect.goMessageSignal.connect(self.show_message)
        self.hello.close()
        self.twoConnect.show()

    def show_multi_host(self):
        # go MultiHostWindow
        # for MultiHostWindow to MultiMessageWindow or HelloWindow
        self.hello.close()
        self.multiHostWindow = MultiHostWindow()
        self.multiHostWindow.show()
        self.multiHostWindow.goBackHelloSignal.connect(self.back_hello_from_multi_host)
        self.multiHostWindow.goMessage0Signal.connect(self.goMessage0)

    def show_multi_client(self):
        self.hello.close()
        self.multiClientWindow = MultiClientWindow()
        self.multiClientWindow.show()
        self.multiClientWindow.goBackHelloSignal.connect(self.back_hello_from_multi_client)
        self.multiClientWindow.goMultiMessageSignal.connect(self.goMessage1)

    def back_hello(self):
        self.hello.show()
        self.twoConnect.close()
        if self.Message2Instance is not None:
            self.Message2Instance.close()

    def back_hello_from_multi_host(self):
        self.hello.show()
        self.multiHostWindow.close()

    def back_hello_from_multi_client(self):
        self.hello.show()
        self.multiClientWindow.close()

    def goMessage0(self, port, nickname):
        self.multiMessageWindow = MultiMessageWindow()
        self.message0 = Message0(port, nickname)
        self.fileServer = Server(port)

        self.multiMessageWindow.sendButtonSignal.connect(self.message0.sendMyMessage)
        self.message0.haveMessageSignal.connect(self.multiMessageWindow.addMoreMessage)
        self.multiMessageWindow.pushButton_3.clicked.connect(self.backMultiHostFromMultiWindow)
        self.multiMessageWindow.sendServer.connect(self.sendMultiFile)

        self.multiMessageWindow.show()
        self.multiHostWindow.close()

    def sendMultiFile(self):
        self.multiMessageWindow.sendMultiFileSignal.connect(self.fileServer.send)
        self.multiMessageWindow.sendButtonSignal.emit("SEND_FILE")

    def goMessage1(self, ip, port, nickname):
        self.multiMessageWindow = MultiMessageWindow()
        self.message1 = Message1(ip, port, nickname)
        self.fileClient = Client(ip, port)

        self.multiMessageWindow.pushButton_2.setEnabled(False)
        self.multiMessageWindow.pushButton_4.setEnabled(False)
        self.multiMessageWindow.sendButtonSignal.connect(self.message1.sendMyMessage)
        self.message1.haveMessageSignal.connect(self.multiMessageWindow.addMoreMessage)
        self.multiMessageWindow.pushButton_3.clicked.connect(self.backMultiClientFromMultiWindow)
        self.multiMessageWindow.receiveMultiFileSignal.connect(self.multiMessageWindow.showReceiveFile)


        self.multiMessageWindow.show()
        self.multiClientWindow.close()

    def backTwoConnectFromMessage(self):
        self.twoConnect.show()
        self.message.close()
        self.Message2Instance.close()
        self.twoConnect.Connecting.hide()

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
        self.message.audioButton.clicked.connect(self.message.startAudioRequest)
        self.message.backButton.clicked.connect(self.backTwoConnectFromMessage)
        self.message.goFileSignal.connect(self.show_file)

        self.Message2Instance.videoDenySignal.connect(self.message.closeVideoRequest)
        self.Message2Instance.recvMessageSignal.connect(self.message.receiveMessage)
        self.Message2Instance.videoRequestSignal.connect(self.message.videoRequestCheck)
        self.Message2Instance.socketReadySignal.connect(self.socket_ok)
        self.Message2Instance.fileRequestSignal.connect(self.message.fileRequestCheck)

        self.Message2Instance.audioRequestSignal.connect(self.message.audioRequestCheck)
        self.message.goAudioSignal.connect(self.show_audio)

    def socket_ok(self):
        self.message.show()
        self.twoConnect.close()

    # File Window
    def show_file(self):
        self.file = FileWindow(self.openPort, self.ipToConnect, self.portToConnect, self.nickName)
        self.file.show()
        self.fileInstance = self.file.fileTransfer
        self.fileInstance.receiveStartSignal.connect(self.file.receiveStart)
        self.fileInstance.receiveEndSignal.connect(self.file.receiveEnd)
        self.fileInstance1 = self.file.fileTransfer1
        self.fileInstance1.receiveStartSignal.connect(self.file.receiveStart)
        self.fileInstance1.receiveEndSignal.connect(self.file.receiveEnd)
        self.file.sendNameSignal.connect(self.send_file)
        self.file.sendFilesNameSignal.connect(self.send_files)

        self.Message2Instance.fileDenySignal.connect(self.file.closeFileRequest)

        self.file.closeFileSignal.connect(self.close_file)
        self.file.closeFileSignal2.connect(self.message.closeFileMsgSend)
        self.Message2Instance.fileCloseMsgSignal.connect(self.file.closeFileMsg)

    def send_file(self, filename):
        fileInstance = self.fileInstance
        fileName = filename
        self.file.videoButton_3.clicked.connect(partial(transfer,fileInstance,fileName))

    def send_files(self, filename):
        fileInstance1 = self.fileInstance1
        fileName = filename
        self.file.videoButton_5.clicked.connect(partial(transfer1,fileInstance1,fileName))

    def close_file(self):
        self.file.close()

    def show_audio(self):
        self.audio = AudioWindow(self.openPort, self.ipToConnect, self.portToConnect)
        self.audio.show()
        self.Message2Instance.audioDenySignal.connect(self.audio.closeAudioRequest)
        self.audio.closeAudioSignal.connect(self.close_audio)
        self.Message2Instance.audioCloseMsgSignal.connect(self.audio.closeAudioMsg)

        self.audio.closeAudioSignal2.connect(self.message.closeAudioMsgSend)

    def close_audio(self):
        self.audio.close()

    def backMultiHostFromMultiWindow(self):
        if self.message0:
            self.message0.close()
        self.multiMessageWindow.close()
        self.multiHostWindow.show()

    def backMultiClientFromMultiWindow(self):
        if self.message1:
            self.message1.close()
        self.multiMessageWindow.close()
        self.multiClientWindow.show()

