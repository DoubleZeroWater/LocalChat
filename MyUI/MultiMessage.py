# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MultiMessage.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class MultiMessageUI(object):
    def setupUi(self, MultiMessageUI):
        MultiMessageUI.setObjectName("MultiMessageUI")
        MultiMessageUI.resize(666, 471)
        self.textBrowser = QtWidgets.QTextBrowser(MultiMessageUI)
        self.textBrowser.setGeometry(QtCore.QRect(0, 10, 501, 381))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(MultiMessageUI)
        self.lineEdit.setGeometry(QtCore.QRect(10, 410, 371, 51))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(MultiMessageUI)
        self.pushButton.setGeometry(QtCore.QRect(400, 410, 101, 51))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(MultiMessageUI)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 10, 131, 71))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(MultiMessageUI)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 390, 131, 71))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(MultiMessageUI)
        self.pushButton_4.setGeometry(QtCore.QRect(520, 120, 131, 71))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(MultiMessageUI)
        QtCore.QMetaObject.connectSlotsByName(MultiMessageUI)

    def retranslateUi(self, MultiMessageUI):
        _translate = QtCore.QCoreApplication.translate
        MultiMessageUI.setWindowTitle(_translate("MultiMessageUI", "MultiMessage"))
        self.pushButton.setText(_translate("MultiMessageUI", "发送"))
        self.pushButton_2.setText(_translate("MultiMessageUI", "进入语音"))
        self.pushButton_3.setText(_translate("MultiMessageUI", "退出"))
        self.pushButton_4.setText(_translate("MultiMessageUI", "文件传输"))
