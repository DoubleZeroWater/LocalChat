# 主窗口
from PyQt5 import QtWidgets, QtCore
from MyUI.LocalChatTools import LocalChatToolsUI
from MyUI.TwoConnect import TwoConnectUI


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

    def __init__(self):
        super(TwoConnectWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.goMainUI)

    def goMainUI(self):
        self.fromTwoConnectToMainSignal.emit()

