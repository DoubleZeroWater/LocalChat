from socket import*
import json
import os
import struct

# 服务器端文件夹位置
FILEPATH = "E:/Pythonproject/"

# 创建sever服务器
sever = socket(AF_INET, SOCK_STREAM)
ip_port = ('192.168.31.190',5354)
buffSize = 1024

# 监听
sever.bind(ip_port)
sever.listen(5)

while True:
    # 连接客户端
    print("waiting for connection......\n")
    clientSock, addr = sever.accept()
    print("connected with ", end = '')
    print(addr)
    print()

    # 开始通信
    while True:
            # 接收客户端发送的报头长度
            head_struct = clientSock.recv(4)

            # 解析报头的长度
            head_len = struct.unpack('i', head_struct)[0]

            # 接收大小为head_len的报头内容（报头内容包括文件大小，文件名内容）
            data = clientSock.recv(head_len)

            # 解析报头的内容, 报头为一个字典其中包含上传文件的大小和文件名，
            head_dir = json.loads(data.decode("utf-8")) # 将JSON字符串解码为python对象
            filesize_b = head_dir["fileSize"]
            fileName = head_dir["fileName"]

            # 接收真实的文件内容
            recv_len = 0
            recv_mesg = b''

            # 在服务器文件夹中创建新文件
            fileInfor = FILEPATH +fileName
            f = open(fileInfor, "wb")

            # 开始接收用户上传的文件
            while recv_len < filesize_b:

                if filesize_b-recv_len > buffSize:
                    # 假设未上传的文件数据大于最大传输数据
                    recv_mesg = clientSock.recv(buffSize)
                    f.write(recv_mesg)
                    recv_len += len(recv_mesg)
                else:
                    # 需要传输的文件数据小于最大传输数据大小
                    recv_mesg = clientSock.recv(filesize_b-recv_len)
                    recv_len += len(recv_mesg)
                    f.write(recv_mesg)
                    f.close()
                    print("文件接收完毕！")

            # 向用户发送信号，文件已经上传完毕
            completed = "1"
            clientSock.send(bytes(completed, "utf-8"))


sever.close()

