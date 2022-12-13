# 主窗口
import time
import tkinter as tk
from multiprocessing import Queue
from time import strftime
from tkinter import filedialog

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent

from Logic.LocalIPGet import getIP
from MyUI.AudioChat import AudioUI
from MyUI.File import FileUI
from MyUI.LocalChatTools import LocalChatToolsUI
from MyUI.Message import MessageUI
from MyUI.MultiClient import MultiClientUI
from MyUI.MultiHost import MultiHostUI
from MyUI.MultiMessage import MultiMessageUI
from MyUI.TwoConnect import TwoConnectUI
from Transfer_File.file_transfer import File_Transfer
from Transfer_File1.file_transfer1 import File_Transfer1
from audio.audio import Audio
from video.vchat import Video_Client, Video_Server

ShareData = Queue()


class HelloWindow(QtWidgets.QMainWindow, LocalChatToolsUI):
    goTwoConnectSignal = QtCore.pyqtSignal()  # 跳转信号
    goMultiConnectSignalHost = QtCore.pyqtSignal()
    goMultiConnectSignalClient = QtCore.pyqtSignal()

    def __init__(self):
        super(HelloWindow, self).__init__()
        self.setupUi(self)
        self.Button2Mode.clicked.connect(self.goTwoConnectUI)
        self.ButtonMutiMode.clicked.connect(self.goMultiConnectUI)

    def goTwoConnectUI(self):
        self.goTwoConnectSignal.emit()

    def goMultiConnectUI(self):

        reply = QtWidgets.QMessageBox.question(self, '多人聊天', '你是否想成为房主？',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.goMultiConnectSignalHost.emit()
        else:
            self.goMultiConnectSignalClient.emit()


# 登录窗口
class TwoConnectWindow(QtWidgets.QMainWindow, TwoConnectUI):
    fromTwoConnectToMainSignal = QtCore.pyqtSignal()  # 跳转信号
    goMessageSignal = QtCore.pyqtSignal(str, str, str, str, object)  # Check if connected

    def __init__(self):
        super(TwoConnectWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.goMainUI)
        self.pushButton.clicked.connect(self.goConnect)
        self.IP.setText(getIP())
        self.Connecting.hide()


    def goMainUI(self):
        self.fromTwoConnectToMainSignal.emit()

    def goConnect(self):
        self.Connecting.show()
        openPort = self.OpenPort.text()
        ipToConnect = self.IPToConnect.text()
        portToConnect = self.PortToConnect.text()
        nickName = self.Nickname.text()
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
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

    def showMessage(self):
        message = self.toSend.toPlainText()
        self.toSend.clear()
        self.sendMessageSignal.emit(f"{self.nickname}  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{message}")
        self.textBrowser.append(f"{self.nickname}  {strftime('%Y/%m/%d %H:%M:%S', time.localtime())}>>\n{message}")

    def receiveMessage(self, message):
        self.textBrowser.append(message)

    def videoRequestCheck(self, ip):
        reply = QtWidgets.QMessageBox.question(self, '视频聊天', '是否接受视频聊天请求？',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.vServer = Video_Server(9632, 4)
            self.vServer.start()
            self.vClient = Video_Client(ip, 9632, 1, 4)
            self.vClient.start()
            self.sendMessageSignal.emit("VIDEO_ACCEPT")
        else:
            self.sendMessageSignal.emit("VIDEO_REFUSE")

    def startVideoRequest(self, ip):
        self.sendMessageSignal.emit("VIDEO_REQUEST")


    def goFileUI(self):
        self.goFileSignal.emit()

    def startFileRequest(self):
        self.sendMessageSignal.emit("FILE_REQUEST")
        self.goFileUI()

    def fileRequestCheck(self):
        reply = QtWidgets.QMessageBox.question(self, '文件传输', '是否同意进行文件传输？',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.goFileUI()
        else:
            self.sendMessageSignal.emit("FILE_DENY")

    def goAudioUI(self):
        self.goAudioSignal.emit()

    def audioRequestCheck(self):
        reply = QtWidgets.QMessageBox.question(self, '音频通话', '是否同意进行音频通话？',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.goAudioUI()
        else:
            self.sendMessageSignal.emit("AUDIO_DENY")

    def startAudioRequest(self):
        self.sendMessageSignal.emit("AUDIO_REQUEST")
        self.goAudioUI()

    def closeFileMsgSend(self):
        self.sendMessageSignal.emit("FILE_CLOSE")

    def closeAudioMsgSend(self):
        self.sendMessageSignal.emit("AUDIO_CLOSE")







class FileWindow(QtWidgets.QMainWindow, FileUI):
    sendNameSignal = pyqtSignal(str)
    sendFilesNameSignal = pyqtSignal(str)
    closeFileSignal = pyqtSignal()
    closeFileSignal2 = pyqtSignal()


    def __init__(self, openPort, ipToConnect, portToConnect, nickname):
        super(FileWindow, self).__init__()
        self.setupUi(self)
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        self.filename = ""
        ip = getIP()
        self.fileTransfer = File_Transfer(ip, 5453, self.ipToConnect, 5453)
        self.fileTransfer1 = File_Transfer1(ip, 5454, self.ipToConnect, 5454)
        self.fileTransfer.start()
        self.fileTransfer1.start()
        self.videoButton_2.clicked.connect(self.fileSend)
        self.videoButton_4.clicked.connect(self.filesSend)
        self.flag=1

    def fileSend(self):
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-alpha", 0)
        fileName = filedialog.askopenfilename(title='选择文件', filetypes=[('EXE', '*.exe'), ('All Files', '*')])
        root.destroy()
        # 输出文件，查看文件路径
        self.filename = fileName.replace('/', '\\')
        self.textBrowser_2.append(">>>您已选取文件：" + self.filename)
        # Thread(target=self.send, args=(self.filename,)).start()
        self.sendNameSignal.emit(self.filename)

    def filesSend(self):
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-alpha", 0)
        fileName = filedialog.askdirectory(title='选择文件夹')
        root.destroy()
        # 输出文件，查看文件路径
        self.filename = fileName.replace('/', '\\')
        self.textBrowser_2.append(">>>您已选取文件夹：" + self.filename)
        # Thread(target=self.send, args=(self.filename,)).start()
        self.sendFilesNameSignal.emit(self.filename)

    def receiveStart(self):
        self.textBrowser_2.append(">>>正在接受文件")

    def receiveProcess(self, process):
        print(process)
        self.textBrowser_2.setText(">>>当前进度为："+process)

    def receiveEnd(self, fileName):
        self.textBrowser_2.append(">>>您已成功接受文件" + fileName)

    def sendEnd(self):
        self.textBrowser_2.append(">>>您已成功发送文件")

    def closeFileRequest(self):
        self.fileTransfer.raise_exception()
        self.fileTransfer1.raise_exception()
        self.closeFileSignal.emit()
        reply = QtWidgets.QMessageBox.information(self, '消息', '你的邀请已被拒绝')
        print(reply)

    def closeFileMsg(self):
        self.fileTransfer.raise_exception()
        self.fileTransfer1.raise_exception()
        reply = QtWidgets.QMessageBox.information(self, '消息', '对方已挂断')
        self.closeFileSignal.emit()

    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        self.fileTransfer.raise_exception()
        self.fileTransfer1.raise_exception()
        self.closeFileSignal.emit()
        if self.flag==1:
            self.closeFileSignal2.emit()
        self.flag=0

    def closeFileMsg(self):
        self.fileTransfer.raise_exception()
        self.fileTransfer1.raise_exception()
        reply = QtWidgets.QMessageBox.information(self, '消息', '对方已断开文件传输')
        self.closeFileSignal.emit()

    def closeFileRequest(self):
        self.fileTransfer.raise_exception()
        self.fileTransfer1.raise_exception()
        reply = QtWidgets.QMessageBox.information(self, '消息', '你的邀请已被拒绝')
        self.closeFileSignal.emit()
        print(reply)

    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        self.fileTransfer.raise_exception()
        self.closeFileSignal.emit()
        if self.flag==1:
            self.closeFileSignal2.emit()
        self.flag=0





class AudioWindow(QtWidgets.QMainWindow, AudioUI):
    closeAudioSignal = pyqtSignal()
    closeAudioSignal2 = pyqtSignal()

    def __init__(self, openPort, ipToConnect, portToConnect):
        super(AudioWindow, self).__init__()
        self.setupUi(self)
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        ip = getIP()
        self.audioConnect = Audio("", ip, 9808, self.ipToConnect, 9808)
        self.audioConnect.start()
        self.videoButton_3.clicked.connect(self.closeAudio)
        self.flag=1


    def closeAudio(self):
        self.audioConnect.raise_exception()
        self.closeAudioSignal.emit()

    def closeAudioMsg(self):
        self.audioConnect.raise_exception()
        reply = QtWidgets.QMessageBox.information(self, '消息', '对方已挂断')
        self.closeAudioSignal.emit()

    def closeAudioRequest(self):
        self.audioConnect.raise_exception()
        reply = QtWidgets.QMessageBox.information(self, '消息', '你的邀请已被拒绝')
        self.closeAudioSignal.emit()
        print(reply)

    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        self.audioConnect.raise_exception()
        self.closeAudioSignal.emit()
        if self.flag==1:
            self.closeAudioSignal2.emit()
        self.flag=0



class MultiHostWindow(QtWidgets.QMainWindow, MultiHostUI):
    goBackHelloSignal = QtCore.pyqtSignal()
    goMessage0Signal = QtCore.pyqtSignal(int, str)  #

    def __init__(self):
        super(MultiHostWindow, self).__init__()
        self.setupUi(self)
        self.lineEdit.setText(getIP())
        self.pushButton.clicked.connect(self.goMessage0)
        self.pushButton_2.clicked.connect(self.goBackHello)

    def goBackHello(self):
        self.goBackHelloSignal.emit()

    def goMessage0(self):
        port = self.lineEdit_2.text()
        nickname = self.lineEdit_3.text()
        self.goMessage0Signal.emit(int(port), nickname)

    def closeMultiHost(self):
        self.close()


class MultiMessageWindow(QtWidgets.QMainWindow, MultiMessageUI):
    sendButtonSignal = QtCore.pyqtSignal(str)
    sendMultiFileSignal = QtCore.pyqtSignal(str)
    sendMyFileSignal = QtCore.pyqtSignal()
    receiveMultiFileSignal = pyqtSignal()
    audioAcceptSignal = pyqtSignal()
    closeWindowSiganl = pyqtSignal()

    def __init__(self):
        super(MultiMessageWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.pushButtonSlot)
        self.pushButton_4.clicked.connect(self.openFile)
        self.fileReceive = None

    def pushButtonSlot(self):
        self.sendButtonSignal.emit(self.lineEdit.text())
        self.lineEdit.setText("")

    def openFile(self):
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-alpha", 0)
        fileName = filedialog.askopenfilename(title='选择文件', filetypes=[('EXE', '*.exe'), ('All Files', '*')])
        root.destroy()
        # 输出文件，查看文件路径
        self.filename = fileName.replace('/', '\\')
        self.textBrowser.append(">>>您已选取文件并发送:" + self.filename)
        self.sendMultiFileSignal.emit(self.filename)
        self.sendMyFileSignal.emit()


    def addMoreMessage(self, message):
        self.textBrowser.append(message)

    def showReceiveFile(self):
        reply = QtWidgets.QMessageBox.question(self, '文件传输', '是否接受房主传输的文件?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.receiveMultiFileSignal.emit()

    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        self.closeWindowSiganl.emit()

    def showCheckAudio(self):
        reply = QtWidgets.QMessageBox.question(self, '音频通话', '是否加入房主的音频通话?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.audioAcceptSignal.emit()

class MultiClientWindow(QtWidgets.QMainWindow, MultiClientUI):
    goBackHelloSignal = QtCore.pyqtSignal()
    goMultiMessageSignal = QtCore.pyqtSignal(str, int, str)

    def __init__(self):
        super(MultiClientWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.goMultiMessage)
        self.pushButton_2.clicked.connect(self.goBackHello)

    def goBackHello(self):
        self.goBackHelloSignal.emit()

    def goMultiMessage(self):
        ip = self.lineEdit.text()
        port = self.lineEdit_2.text()
        nickname = self.lineEdit_3.text()
        self.goMultiMessageSignal.emit(ip, int(port), nickname)

