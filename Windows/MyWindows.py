# 主窗口
import os
from functools import partial
from multiprocessing import Queue

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog

from Logic.LocalIPGet import getIP
from MyUI.File import FileUI
from MyUI.LocalChatTools import LocalChatToolsUI
from MyUI.Message import MessageUI
from MyUI.TwoConnect import TwoConnectUI
from Transfer_File.file_transfer import File_Transfer
from video.vchat import Video_Client, Video_Server

ShareData = Queue()


class HelloWindow(QtWidgets.QMainWindow, LocalChatToolsUI):
    goTwoConnectSignal = QtCore.pyqtSignal()  # 跳转信号

    def __init__(self):
        super(HelloWindow, self).__init__()
        self.setupUi(self)
        self.Button2Mode.clicked.connect(self.goTwoConnectUI)

    def goTwoConnectUI(self):
        self.goTwoConnectSignal.emit()


# 登录窗口
class TwoConnectWindow(QtWidgets.QMainWindow, TwoConnectUI):
    fromTwoConnectToMainSignal = QtCore.pyqtSignal()  # 跳转信号
    goMessageSignal = QtCore.pyqtSignal(str, str, str, str, object)  # Check if connected

    def __init__(self):
        super(TwoConnectWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.goMainUI)
        self.pushButton.clicked.connect(self.goConnect)
        self.currentIP.setHtml(f"你的当前IP是:{getIP()}")
        self.label_4.hide()

    def goMainUI(self):
        self.fromTwoConnectToMainSignal.emit()

    def goConnect(self):
        self.label_4.show()
        openPort = self.openPort.toPlainText()
        ipToConnect = self.ipToConnect.toPlainText()
        portToConnect = self.portToConnect.toPlainText()
        nickName = self.nickNameInput.toPlainText()
        self.goMessageSignal.emit(openPort, ipToConnect, portToConnect, nickName, ShareData)


class MessageWindow(QtWidgets.QMainWindow, MessageUI):
    sendMessageSignal = pyqtSignal(str)
    goFileSignal = pyqtSignal()
    nickname = None

    def __init__(self):
        super(MessageWindow, self).__init__()
        self.vClient = None
        self.vServer = None
        self.setupUi(self)
        self.sendButton.clicked.connect(self.showMessage)

    def showMessage(self):
        message = self.toSend.toPlainText()
        self.toSend.clear()
        self.sendMessageSignal.emit(f"{self.nickname} >>:  {message}")
        self.textBrowser.append(f"{self.nickname} >>:  {message}")

    def receiveMessage(self, message):
        self.textBrowser.append(message)

    def videoRequestCheck(self, ip):
        reply = QtWidgets.QMessageBox.question(self, '视频聊天', '是否接受视频聊天请求？',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.vServer = Video_Server(9632,4)
            self.vServer.start()
            self.vClient = Video_Client(ip, 9632, 1, 4)
            self.vClient.start()
        else:
            self.sendMessageSignal.emit("VIDEO_DENY")

    def startVideoRequest(self,ip):
        self.vServer = Video_Server(9632, 4)
        self.vServer.start()
        self.vClient = Video_Client(ip, 9632, 1, 4)
        self.vClient.start()
        self.sendMessageSignal.emit("VIDEO_REQUEST")

    def closeVideoRequest(self):
        self.vServer.raise_exception()
        self.vClient.raise_exception()

    def goFileUI(self):
        self.goFileSignal.emit()

    def fileRequestCheck(self):
        reply = QtWidgets.QMessageBox.question(self, '文件传输', '是否同意进行文件传输？',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.goFileUI()
        else:
            self.sendMessageSignal.emit("FILE_DENY")

    def startFileRequest(self):
        self.sendMessageSignal.emit("FILE_REQUEST")
        self.goFileUI()

    def closeFileRequest(self):
        reply = QtWidgets.QMessageBox.information(self, "Information", "对方已拒绝", QMessageBox.Ok)
        print(reply)

class FileWindow(QtWidgets.QMainWindow, FileUI):

    def __init__(self,openPort, ipToConnect, portToConnect, nickname):
        super(FileWindow, self).__init__()
        self.setupUi(self)
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        self.nickname = nickname
        ip = getIP()
        self.fileTransfer = File_Transfer(self.ipToConnect, 5453, ip, 5453)
        self.fileTransfer.start()
        self.videoButton_2.clicked.connect(self.fileSend)



    def fileSend(self):
        fileName = QFileDialog.getOpenFileName(self, '选择文件', os.getcwd(), "All Files(*);;Text Files(*.txt)")
        # 输出文件，查看文件路径
        name1 = fileName[0]
        name = name1.replace('/', '\\')
        self.textBrowser_2.append(">>>您已成功发送文件：" + name)
        Thread(target=File_Transfer.send,args=name).start()

    def closeFileRequest(self):
        self.fileTransfer.raise_exception()

    def receiveStart(self):
        self.textBrowser_2.append(">>>正在接受文件")

    def receiveEnd(self, fileName):
        self.textBrowser_2.append(">>>您已成功接受文件"+fileName)
    #
    # def uploadFile(self,openPort, ipToConnect, portToConnect)
    #
    #     self.fileTransfer = File_Transfer("", self.ipToConnect, 5453, self.ip, 5453)
    #     self.fileTransfer.client()
    #     self.fileTransfer.server()
    #     self.sendFileSignal.emit("File_REQUEST")
    #     self.textBrowser_2.append(">>>"+ip+"已成功发送文件："+name+"至"+ipToConnect)
