# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TwoConnect.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class TwoConnectUI(object):
    def setupUi(self, TwoConnectUI):
        TwoConnectUI.setObjectName("TwoConnectUI")
        TwoConnectUI.resize(723, 510)
        self.pushButton = QtWidgets.QPushButton(TwoConnectUI)
        self.pushButton.setGeometry(QtCore.QRect(510, 400, 161, 81))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(TwoConnectUI)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 400, 151, 81))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setAutoRepeat(False)
        self.pushButton_2.setAutoExclusive(False)
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.Connecting = QtWidgets.QLabel(TwoConnectUI)
        self.Connecting.setGeometry(QtCore.QRect(300, 420, 141, 51))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.Connecting.setFont(font)
        self.Connecting.setObjectName("Connecting")
        self.OpenPort = QtWidgets.QLineEdit(TwoConnectUI)
        self.OpenPort.setGeometry(QtCore.QRect(460, 310, 211, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.OpenPort.setFont(font)
        self.OpenPort.setObjectName("OpenPort")
        self.IPToConnect = QtWidgets.QLineEdit(TwoConnectUI)
        self.IPToConnect.setGeometry(QtCore.QRect(460, 250, 211, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.IPToConnect.setFont(font)
        self.IPToConnect.setText("")
        self.IPToConnect.setObjectName("IPToConnect")
        self.PortToConnect = QtWidgets.QLineEdit(TwoConnectUI)
        self.PortToConnect.setGeometry(QtCore.QRect(460, 190, 211, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.PortToConnect.setFont(font)
        self.PortToConnect.setObjectName("PortToConnect")
        self.Nickname = QtWidgets.QLineEdit(TwoConnectUI)
        self.Nickname.setGeometry(QtCore.QRect(460, 130, 211, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.Nickname.setFont(font)
        self.Nickname.setText("")
        self.Nickname.setObjectName("Nickname")
        self.IP = QtWidgets.QLineEdit(TwoConnectUI)
        self.IP.setGeometry(QtCore.QRect(460, 70, 211, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.IP.setFont(font)
        self.IP.setText("")
        self.IP.setObjectName("IP")
        self.layoutWidget = QtWidgets.QWidget(TwoConnectUI)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 70, 255, 281))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)

        self.retranslateUi(TwoConnectUI)
        QtCore.QMetaObject.connectSlotsByName(TwoConnectUI)

    def retranslateUi(self, TwoConnectUI):
        _translate = QtCore.QCoreApplication.translate
        TwoConnectUI.setWindowTitle(_translate("TwoConnectUI", "Form"))
        self.pushButton.setText(_translate("TwoConnectUI", "确定连接"))
        self.pushButton_2.setText(_translate("TwoConnectUI", "返回"))
        self.Connecting.setText(_translate("TwoConnectUI", "正在连接中..."))
        self.OpenPort.setText(_translate("TwoConnectUI", "22222"))
        self.PortToConnect.setText(_translate("TwoConnectUI", "22222"))
        self.label_6.setText(_translate("TwoConnectUI", "你的当前IP是:"))
        self.label_5.setText(_translate("TwoConnectUI", "你的昵称是:"))
        self.label.setText(_translate("TwoConnectUI", "你想要连接的端口是："))
        self.label_2.setText(_translate("TwoConnectUI", "你想要连接的IP是："))
        self.label_3.setText(_translate("TwoConnectUI", "你想要开放连接端口是："))
