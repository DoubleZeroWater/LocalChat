import ctypes
import json
import os
import struct
from socket import *
from threading import Thread

# 服务端 发送
class Server():
    def __init__(self, openPort):
        super().__init__()
        self.openPort = openPort

    def server_socket(self, filename: str):
        try:
            print(self.openPort)
            self.sever = socket(AF_INET, SOCK_STREAM)
            ip_port = ("", self.openPort)
            # 监听
            self.sever.bind(ip_port)
            self.sever.listen()
            while True:
                self.severSock, addr = self.sever.accept()
                Thread(target=self.send, args=(filename,)).start()
        except IOError:
            pass
        except:
            pass

    def send(self, filename):
        buffSize = 1024
        # 上传文件
        fileInfor = filename
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
        self.severSock.send(head_infor_len)
        self.severSock.send(head_infor.encode("utf-8"))
        # 发送真实文件
        with open(fileInfor, 'rb') as f:
            data = f.read()
            self.severSock.sendall(data)
            f.close()
        # 客户端若接受完文件会发送信号，服务端接收
        completed = self.severSock.recv(buffSize).decode("utf-8")
        if completed == "1":
            print("发送成功")

    def killAllBugs(self,filename: str):
        Thread(target=self.server_socket,args=(filename,)).start()


if __name__ == '__main__':
    sender = Server(22222)
    sender.killAllBugs(r'E:\test\123\1235.txt')