# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow


class TwoConnectUI(object):
    def setupUi(self, TwoConnectUI):
        TwoConnectUI.setObjectName("TwoConnectUI")
        TwoConnectUI.resize(400, 300)
        self.currentIP = QtWidgets.QTextBrowser(TwoConnectUI)
        self.currentIP.setGeometry(QtCore.QRect(30, 60, 351, 31))
        self.currentIP.setObjectName("currentIP")
        self.connectPort = QtWidgets.QTextEdit(TwoConnectUI)
        self.connectPort.setGeometry(QtCore.QRect(220, 110, 161, 31))
        self.connectPort.setObjectName("connectPort")
        self.label = QtWidgets.QLabel(TwoConnectUI)
        self.label.setGeometry(QtCore.QRect(30, 110, 141, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(TwoConnectUI)
        self.label_2.setGeometry(QtCore.QRect(30, 150, 141, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(TwoConnectUI)
        self.label_3.setGeometry(QtCore.QRect(30, 190, 161, 31))
        self.label_3.setObjectName("label_3")
        self.connectIP = QtWidgets.QTextEdit(TwoConnectUI)
        self.connectIP.setGeometry(QtCore.QRect(220, 150, 161, 31))
        self.connectIP.setObjectName("connectIP")
        self.openPort = QtWidgets.QTextEdit(TwoConnectUI)
        self.openPort.setGeometry(QtCore.QRect(220, 190, 161, 31))
        self.openPort.setObjectName("openPort")
        self.pushButton = QtWidgets.QPushButton(TwoConnectUI)
        self.pushButton.setGeometry(QtCore.QRect(260, 250, 93, 28))
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(TwoConnectUI)
        self.pushButton_2.setGeometry(QtCore.QRect(80, 250, 93, 28))
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setAutoRepeat(False)
        self.pushButton_2.setAutoExclusive(False)
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(TwoConnectUI)
        QtCore.QMetaObject.connectSlotsByName(TwoConnectUI)

    def retranslateUi(self, TwoConnectUI):
        _translate = QtCore.QCoreApplication.translate
        TwoConnectUI.setWindowTitle(_translate("TwoConnectUI", "Form"))
        self.currentIP.setHtml(_translate("TwoConnectUI",
                                          "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                          "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                          "p, li { white-space: pre-wrap; }\n"
                                          "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                          "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">你的当前IP是:</p></body></html>"))
        self.connectPort.setHtml(_translate("TwoConnectUI",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText(_translate("TwoConnectUI", "你想要连接的端口是："))
        self.label_2.setText(_translate("TwoConnectUI", "你想要连接的IP是："))
        self.label_3.setText(_translate("TwoConnectUI", "你想要开放连接端口是："))
        self.connectIP.setHtml(_translate("TwoConnectUI",
                                          "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                          "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                          "p, li { white-space: pre-wrap; }\n"
                                          "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                          "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.openPort.setHtml(_translate("TwoConnectUI",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                         "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton.setText(_translate("TwoConnectUI", "确定连接"))
        self.pushButton_2.setText(_translate("TwoConnectUI", "返回"))
