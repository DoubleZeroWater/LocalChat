from Windows.MyWindows import HelloWindow, TwoConnectWindow


class Controller:
    def __init__(self):
        self.hello = None
        self.login = None

    # 跳转到 hello 窗口
    def show_hello(self):
        self.hello = HelloWindow()
        self.hello.goTwoConnectSignal.connect(self.show_two_connect)
        self.hello.show()

    # 跳转到 login 窗口, 注意关闭原页面
    def show_two_connect(self):
        self.login = TwoConnectWindow()
        self.login.fromTwoConnectToMainSignal.connect(self.back_hello)
        self.hello.close()
        self.login.show()

    def back_hello(self):
        self.hello.show()
        self.login.close()
