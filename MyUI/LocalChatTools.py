# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LocalChatTools.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class LocalChatTools(object):
    def setupUi(self, LocalChatTools):
        LocalChatTools.setObjectName("LocalChatTools")
        LocalChatTools.resize(600, 558)
        self.Button2Mode = QtWidgets.QPushButton(LocalChatTools)
        self.Button2Mode.setGeometry(QtCore.QRect(200, 270, 201, 101))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.Button2Mode.setFont(font)
        self.Button2Mode.setObjectName("Button2Mode")
        self.ButtonMutiMode = QtWidgets.QPushButton(LocalChatTools)
        self.ButtonMutiMode.setGeometry(QtCore.QRect(200, 400, 201, 91))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.ButtonMutiMode.setFont(font)
        self.ButtonMutiMode.setObjectName("ButtonMutiMode")
        self.label = QtWidgets.QLabel(LocalChatTools)
        self.label.setGeometry(QtCore.QRect(180, 120, 321, 111))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(LocalChatTools)
        QtCore.QMetaObject.connectSlotsByName(LocalChatTools)

    def retranslateUi(self, LocalChatTools):
        _translate = QtCore.QCoreApplication.translate
        LocalChatTools.setWindowTitle(_translate("LocalChatTools", "LocalChatTools"))
        self.Button2Mode.setText(_translate("LocalChatTools", "双人通信模式"))
        self.ButtonMutiMode.setText(_translate("LocalChatTools", "多人群聊模式"))
        self.label.setText(_translate("LocalChatTools", "LocalChatTools"))
