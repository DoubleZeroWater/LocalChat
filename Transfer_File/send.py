from socket import*
import struct
import json
import os
import sys
import time

# 用户的文件夹路径
FILEPATH = "E:/Pythonproject/file_transfer-master/"

# 创建客户端
client = socket(AF_INET, SOCK_STREAM)
ip_port = ('192.168.31.190', 5354)
buffSize = 1024
client.connect(ip_port)
print("connecting...")

# 开始通信
while True:
    # 上传文件
    fileName = input("请输入要上传的文件名加后缀：").strip()
    fileInfor = FILEPATH + fileName

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
    client.send(head_infor_len)
    client.send(head_infor.encode("utf-8"))

    # 发送真实文件
    with open(fileInfor, 'rb') as f:
        data = f.read()
        client.sendall(data)
        f.close()

    # 服务器若接受完文件会发送信号，客户端接收
    completed = client.recv(buffSize).decode("utf-8")
    if completed == "1":
        print("发送成功")