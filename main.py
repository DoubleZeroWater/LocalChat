import sys

from PyQt5 import QtWidgets

from Windows.Controller import Controller

if __name__ == '__main__':
    # import reInterpreter as inter
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()  # 控制器实例
    controller.show_hello()  # 默认展示的是 hello 页面
    sys.exit(app.exec_())

#if __name__ == '__main__':
    # import reInterpreter as inter
    #ui = UI()