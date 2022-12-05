# import sys
# from socket import socket, AF_INET, SOCK_STREAM
# from threading import Thread
# from time import strftime, gmtime, sleep
#
# from PyQt5.QtCore import QThread, pyqtSignal
#
#
# class Message3(QThread):
#     fileRequestSignal = pyqtSignal(str)
#     fileDenySignal = pyqtSignal()
#     def __init__(self, openPort: int, ipToConnect: str, portToConnect: int, nickName: str):
#         super(Message3, self).__init__()
#         self.serverInstant = None
#         self.clientInstant = None
#         self.connect_end = None
#         self.openPort = 13245
#         self.ipToConnect = ipToConnect
#         self.portToConnect = 54231
#         self.nickName = nickName
#
#     def run(self):
#         Thread(target=self.server).start()
#         Thread(target=self.client).start()
#
#     def client(self):
#         self.clientInstant = socket(AF_INET, SOCK_STREAM)
#         while 1:
#             try:
#                 self.clientInstant.connect((self.ipToConnect, self.portToConnect))
#             except ConnectionRefusedError:
#                 sleep(2)
#                 print("Connect Fail.")
#                 continue
#             else:
#                 break
#
#     def server(self):
#         print("111")
#         self.serverInstant = socket(AF_INET, SOCK_STREAM)
#         self.serverInstant.bind(('', self.openPort))
#         self.serverInstant.listen(60)
#         self.conn, self.addr = self.serverInstant.accept()
#         while not self.connect_end:
#             recv_data = self.conn.recv(1024).decode('utf-8')
#             print(recv_data)
#             if recv_data == "##":
#                 # 自身连接
#                 self.clientInstant.close()
#                 self.serverInstant.close()
#                 self.connect_end = True
#                 print('\n---> 与 {} 断开的连接已中断... '.format(self.addr))
#                 sys.exit(0)
#                 break
#             elif recv_data == "FILE_REQUEST":
#                 self.fileRequestSignal.emit(self.ipToConnect)
#             elif recv_data == "FILE_DENY":
#                 self.fileDenySignal.emit()
#

