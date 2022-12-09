import ctypes
import json
import socket
import os
import sys
import struct
import tarfile
import time
from threading import Thread
from socket import *
from PyQt5.QtCore import QThread, pyqtSignal

# 接收端的路径
FILEPATH = "E:/test/"

class File_Transfer1(QThread):
    receiveStartSignal = pyqtSignal()
    receiveEndSignal = pyqtSignal(str)

    def __init__(self, ip, openPort, ipToConnect, portToConnect):
        super(File_Transfer1, self).__init__()
        self.openPort = openPort
        self.ipToConnect = ipToConnect
        self.portToConnect = portToConnect
        # self.name = name
        self.ip = ip
        self.clint = None

    def run(self):
        Thread(target=self.server).start()
        Thread(target=self.client).start()

    def server(self):
        ip_port = ("", self.openPort)
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.bind(ip_port)
            s.listen(2)
        except error as msg:
            print(msg)
            sys.exit(1)
        print('waiting..............')
        self.clientSock, addr = s.accept()
        Thread(target=self.receive).start()

    def client(self):
        # 创建客户端
        self.clint = socket(AF_INET, SOCK_STREAM)
        ip_port = (self.ipToConnect, self.portToConnect)
        self.clint.connect(ip_port)
        print("connecting...")

    def receive(self):
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
                    print(f"{recv_len / filesize_b}")
                else:
                    # 需要传输的文件数据小于最大传输数据大小
                    recv_mesg = self.clientSock.recv(filesize_b - recv_len)
                    recv_len += len(recv_mesg)
                    f.write(recv_mesg)
                    f.close()
                    print("文件接收完毕！")
            tar_path = os.walk(FILEPATH)
            for path, dir_list, file_list in tar_path:
                for dir_name in file_list:
                    tarname = os.path.join(path, dir_name)
                    if os.path.splitext(tarname)[-1] == '.tar':
                        # print('TRUE')
                        tar = tarfile.open(tarname, 'r:')
                        file_names = tar.getnames()
                        for file_name in file_names:
                            tar.extract(file_name, FILEPATH)
                        tar.close()
                        # print('tarfile extented')
                        os.remove(tarname)
                        # print('tarfile deleted')
            # 向用户发送信号，文件已经上传完毕
            completed = "1"
            self.clientSock.send(bytes(completed, "utf-8"))
            self.receiveEndSignal.emit(fileName)

    def send(self, filename):
        buffSize = 1024
        fileInfor = filename
        num = fileInfor.rfind('\\')
        fileName = fileInfor[num + 1:]
        # 打包路径
        fileName = fileName + '.tar'
        with tarfile.open(fileName, 'w') as tar:
            tar.add(fileInfor, arcname=os.path.basename(fileInfor))
        fileSize_bytes = os.stat(fileName).st_size
        # 创建字典用于报头
        dirc = {"fileName": fileName,
                "fileSize": fileSize_bytes}
        # 将字典转为JSON字符，再将字符串的长度打包
        head_infor = json.dumps(dirc)
        head_infor_len = struct.pack('i', len(head_infor))
        # 先发送报头长度，然后发送报头内容
        self.clint.send(head_infor_len)
        self.clint.send(head_infor.encode("utf-8"))
        # 发送真实文件
        with open(fileName, 'rb') as f:
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


if __name__ == '__main__':
     file_Transfer = File_Transfer1("192.168.198.152", 5354, "192.168.198.190", 5354)
     file_Transfer.run()
     time.sleep(5)
     file_Transfer.send(r"E:\PycharmPythonProject\U-2-Net-master1.zip")