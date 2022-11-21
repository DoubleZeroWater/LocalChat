from PyQt5.QtWidgets import QApplication
from MyUI.TwoConnect import TwoConnectUI
import sys
import argparse

from Windows.Controller import Controller
from message.UI_message import Messager
from PyQt5 import QtCore, QtWidgets

def argu_setting():
    # 参数设置
    parser = argparse.ArgumentParser()
    sender_ip = "127.0.0.1"
    parser.add_argument('--sender_ip', type=str, default=sender_ip)
    parser.add_argument('--port', type=int, default=10087)
    parser.add_argument('-v', '--version', type=int, default=4)
    args = parser.parse_args()
    SENDER_IP = args.sender_ip
    PORT = args.port
    VERSION = args.version
    msg = Messager(SENDER_IP, PORT, VERSION)
    # diag=Dialog.Dialog()#声明窗口类
    # diag.get_thread(Msg,)#把线程传给窗口，以便重写窗口类
    msg.start()


class UI(object):
    def __init__(self):
        argu_setting()


if __name__ == '__main__':
    # import reInterpreter as inter
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()  # 控制器实例
    controller.show_hello()  # 默认展示的是 hello 页面
    sys.exit(app.exec_())

#if __name__ == '__main__':
    # import reInterpreter as inter
    #ui = UI()