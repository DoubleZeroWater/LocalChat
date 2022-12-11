import ctypes
import json
import os
import struct
from socket import *
from threading import Thread

from PyQt5.QtCore import QThread, pyqtSignal

FILEPATH = "./data/"

class Client():
    receiveStartSignal = pyqtSignal()
    receiveEndSignal = pyqtSignal(str)

    def __init__(self, ipToConnect, portToConnect):
        super().__init__()
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect

    def killEveryBug(self):
        Thread(target=self.client_socket).start()

    def client_socket(self):
        # 创建客户端
        self.clint = socket(AF_INET, SOCK_STREAM)
        ip_port = (self.ipToConnect, self.portToConnect)
        self.clint.connect(ip_port)
        # print("{0} connecting...".format(self.ip))
        # 接收文件
        # while True:
        # 接收客户端发送的报头长度
        buffSize = 1024
        head_struct = self.clint.recv(4)
        # 解析报头的长度
        head_len = struct.unpack('i', head_struct)[0]
        # 接收大小为head_len的报头内容（报头内容包括文件大小，文件名内容）
        data = self.clint.recv(head_len)
        # self.receiveStartSignal.emit()
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
                recv_mesg = self.clint.recv(buffSize)
                f.write(recv_mesg)
                recv_len += len(recv_mesg)
                print(f"{recv_len / filesize_b}")
            else:
                # 需要传输的文件数据小于最大传输数据大小
                recv_mesg = self.clint.recv(filesize_b - recv_len)
                recv_len += len(recv_mesg)
                f.write(recv_mesg)
                f.close()
                print("文件接收完毕！")
        # 向用户发送信号，文件已经上传完毕
        completed = "1"
        self.clint.send(bytes(completed, "utf-8"))
        # self.receiveEndSignal.emit(fileName)
        self.clint.close()

if __name__ == '__main__':
    fileInstance = Client('192.168.43.32',22222)
    fileInstance.killEveryBug()
