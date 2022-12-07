from socket import *
from threading import Thread
import struct
import json
import os
import sys
import time
import ctypes

from PyQt5.QtCore import QThread, pyqtSignal

# 接收端的路径
FILEPATH = "E:/test/"


class File_Transfer(QThread):
    receiveStartSignal = pyqtSignal()
    receiveEndSignal = pyqtSignal(str)

    def __init__(self, ip, openPort, ipToConnect, portToConnect):
        super(File_Transfer, self).__init__()
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        # self.name = name
        self.ip = ip

    def run(self):
        Thread(target=self.server).start()
        Thread(target=self.client).start()

    def server(self):
        sever = socket(AF_INET, SOCK_STREAM)
        ip_port = ("", self.openPort)
        # 监听
        sever.bind(ip_port)
        sever.listen()
        self.clientSock, addr = sever.accept()

    # while True:
    # 	# 连接客户端
    # 	self.receive(sever)
    # sever.close()

    def client(self):
        # 创建客户端
        self.clint = socket(AF_INET, SOCK_STREAM)
        ip_port = (self.ipToConnect, self.portToConnect)
        self.clint.connect(ip_port)
        print("connecting...")

    # 开始通信
    # while True:
    # self.send(clint)
    # clint.close()

    def receive(self, sever: socket):
        # print("waiting for connection......\n")
        # clientSock, addr = sever.accept()
        # 开始通信
        while True:
            # 接收客户端发送的报头长度
            buffSize = 1024
            head_struct = self.clientSock.recv(4)
            # 解析报头的长度
            head_len = struct.unpack('i', head_struct)[0]
            # 接收大小为head_len的报头内容（报头内容包括文件大小，文件名内容）
            data = self.clientSock.recv(head_len)
            self.receiveStartSignal.emit()
            # 解析报头的内容, 报头为一个字典其中包含上传文件的大小和文件名，
            head_dir = json.loads(data.decode("utf-8"))  # 将JSON字符串解码为python对象
            filesize_b = head_dir["fileSize"]
            fileName = head_dir["fileName"]
            # 接收真实的文件内容
            recv_len = 0
            recv_mesg = b''
            # 在服务器文件夹中创建新文件
            fileInfor = FILEPATH + fileName
            f = open(fileInfor, "wb")
            # 开始接收用户上传的文件
            while recv_len < filesize_b:
                if filesize_b - recv_len > buffSize:
                    # 假设未上传的文件数据大于最大传输数据
                    recv_mesg = self.clientSock.recv(buffSize)
                    f.write(recv_mesg)
                    recv_len += len(recv_mesg)
                else:
                    # 需要传输的文件数据小于最大传输数据大小
                    recv_mesg = self.clientSock.recv(filesize_b - recv_len)
                    recv_len += len(recv_mesg)
                    f.write(recv_mesg)
                    f.close()
                    print("文件接收完毕！")
            # 向用户发送信号，文件已经上传完毕
            completed = "1"
            self.clientSock.send(bytes(completed, "utf-8"))
            self.receiveEndSignal.emit(fileName)

    # self.clientSock.close()
    # break

    def send(self, name: str):
        buffSize = 1024
        # 上传文件
        fileInfor = name
        num = fileInfor.rfind('\\')
        fileName = fileInfor[num + 1:]
        # 得到文件的大小
        filesize_bytes = os.path.getsize(fileInfor)
        # 创建复制文件
        fileName = "new" + fileName
        # 创建字典用于报头
        dirc = {"fileName": fileName,
                "fileSize": filesize_bytes}
        # 将字典转为JSON字符，再将字符串的长度打包
        head_infor = json.dumps(dirc)
        head_infor_len = struct.pack('i', len(head_infor))
        # 先发送报头长度，然后发送报头内容
        self.clint.send(head_infor_len)
        self.clint.send(head_infor.encode("utf-8"))
        # 发送真实文件
        with open(fileInfor, 'rb') as f:
            data = f.read()
            self.clint.sendall(data)
            f.close()
        # 服务器若接受完文件会发送信号，客户端接收
        completed = self.clint.recv(buffSize).decode("utf-8")
        if completed == "1":
            print("发送成功")
    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id  # type: ignore
        for id, thread in threading._active.items():  # type: ignore
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        # 精髓就是这句话，给线程发过去一个exceptions，线程就那边响应完就停了
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

# if __name__ == '__main__':
# 	sev = File_Server(5353,"192.168.31.190",5353)
# 	sev.start()
# 	clt = File_Client(r"E:\Pythonproject\LocalChat\video\achat.py","192.168.31.190",5353,"192.168.31.190",5353)
# 	clt.start()
# 	trans = File_Transfer(r"E:\Pythonproject\LocalChat\video\achat.py","172.20.10.9",5453,"172.20.10.3",5453)
# 	trans.start()
