# 主窗口
import os
import time
from multiprocessing import Queue
from threading import Thread

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog

from Logic.LocalIPGet import getIP
from Logic.Message2 import Message2
from MyUI.LocalChatTools import LocalChatToolsUI
from MyUI.Message import MessageUI
from MyUI.TwoConnect import TwoConnectUI
from video.vchat import Video_Client, Video_Server
from MyUI.File import FileUI
from Transfer_File.file_transfer import File_Client,File_Server
from functools import partial

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
    goFileSignal = QtCore.pyqtSignal()
    nickname = None

    def __init__(self):
        super(MessageWindow, self).__init__()
        self.vClient = None
        self.vServer = None
        self.setupUi(self)
        self.sendButton.clicked.connect(self.showMessage)
        self.FileButton.clicked.connect(self.goFileUI)

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



class FileWindow(QtWidgets.QMainWindow, FileUI):
    sendFileSignal = pyqtSignal(str)

    def __init__(self,openPort, ipToConnect, portToConnect):
        super(FileWindow, self).__init__()
        self.setupUi(self)
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        self.videoButton_2.clicked.connect(partial(self.uploadFile, openPort, ipToConnect, portToConnect))
        print(openPort, ipToConnect, portToConnect)


    def uploadFile(self,openPort, ipToConnect, portToConnect):
        fileName = QFileDialog.getOpenFileName(self, '选择文件', os.getcwd(), "All Files(*);;Text Files(*.txt)")
        # 输出文件，查看文件路径
        name1=fileName[0]
        name =name1.replace('/', '\\')
        print(name)
        ip=getIP()
        print(ip)

        self.fServer = File_Server(int(openPort), ipToConnect, int(portToConnect))
        self.fServer.run()
        self.fClient = File_Client(name, ip, int(openPort), ipToConnect, int(portToConnect))
        self.fClient.run()
        self.sendFileSignal.emit("File_REQUEST")
        self.textBrowser_2.append(">>>"+ip+"已成功发送文件："+name+"至"+ipToConnect)




