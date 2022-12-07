# 主窗口
import os
from functools import partial
from multiprocessing import Queue
from threading import Thread
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog

from Logic.LocalIPGet import getIP
from MyUI.File import FileUI
from MyUI.LocalChatTools import LocalChatToolsUI
from MyUI.Message import MessageUI
from MyUI.TwoConnect import TwoConnectUI
from MyUI.AudioChat import AudioUI
from Transfer_File.file_transfer import File_Transfer
from video.vchat import Video_Client, Video_Server

import tkinter as tk
from tkinter import filedialog

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
    goAudioSignal = pyqtSignal()
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


    def goAudioUI(self):
        self.goAudioSignal.emit()

    def audioRequestCheck(self):
        reply = QtWidgets.QMessageBox.question(self, '语音通话', '是否同意进行语音通话？',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.goAudioUI()
        else:
            self.sendMessageSignal.emit("AUDIO_DENY")

    def startAudioRequest(self):
        self.sendMessageSignal.emit("AUDIO_REQUEST")
        self.goAudioUI()

    def closeAudioRequest(self):
        self.audioConnect.raise_exception()
        reply = QtWidgets.QMessageBox.information(self.toolButton, '消息', '你的邀请已被拒绝')
        print(reply)

    def closeFileRequest(self):
        self.fileTransfer.raise_exception()
        reply = QtWidgets.QMessageBox.information(self.toolButton, '消息', '你的邀请已被拒绝')
        print(reply)


class FileWindow(QtWidgets.QMainWindow, FileUI):
    sendNameSignal = pyqtSignal(str)

    def __init__(self,openPort, ipToConnect, portToConnect, nickname):
        super(FileWindow, self).__init__()
        self.setupUi(self)
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        self.filename = ""
        ip = getIP()
        self.fileTransfer = File_Transfer(ip, 5453, self.ipToConnect, 5453)
        self.fileTransfer.start()
        self.videoButton_2.clicked.connect(self.fileSend)


    def fileSend(self):
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-alpha", 0)
        fileName = filedialog.askopenfilename(root, title='选择文件', filetypes=[('EXE', '*.exe'), ('All Files', '*')])
        root.destroy()
        # 输出文件，查看文件路径
        name1 = fileName[0]
        self.filename = name1.replace('/', '\\')
        self.textBrowser_2.append(">>>您已选取文件：" + self.filename + "请点击发送键")
        self.sendNameSignal.emit(self.filename)

    def receiveStart(self):
        self.textBrowser_2.append(">>>正在接受文件")

    def receiveEnd(self, fileName):
        self.textBrowser_2.append(">>>您已成功接受文件"+fileName)

class AudioWindow(QtWidgets.QMainWindow, AudioUI):

    def __init__(self,openPort, ipToConnect, portToConnect):
        super(AudioWindow, self).__init__()
        self.setupUi(self)
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        ip = getIP()
        self.audioConnect = Audio("", ip, 9808,  self.ipToConnect, 9808)
        self.audioConnect.start()
        self.videoButton_3.clicked.connect(self.closeAudio)



    def closeAudio(self):
        self.audioConnect.raise_exception()