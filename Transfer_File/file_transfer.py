from socket import*
from threading import Thread
import struct
import json
import os
import sys
import time

# 接收端的路径
FILEPATH = "./test/"

# 服务器端
class File_Server(Thread):

	def __init__(self,openPort,ipToConnect,portToConnect):
		super().__init__()
		self.openPort=5353
		self.ipToConnect=5353
		self.portToConnect=5353

	def run(self):
		Thread(target=self.server).start()

	def server(self):
		# 创建sever服务器
		sever = socket(AF_INET, SOCK_STREAM)
		ip_port = ("", 5353)
		buffSize = 1024
		# 监听
		sever.bind(ip_port)
		sever.listen(5)
		while True:
			# 连接客户端
			print("waiting for connection......\n")
			clientSock, addr = sever.accept()
			# print("connected with ", end='')
			# print(addr)
			# print()
			# 开始通信
			while True:
				# 接收客户端发送的报头长度
				head_struct = clientSock.recv(4)
				# 解析报头的长度
				head_len = struct.unpack('i', head_struct)[0]
				# 接收大小为head_len的报头内容（报头内容包括文件大小，文件名内容）
				data = clientSock.recv(head_len)
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
						recv_mesg = clientSock.recv(buffSize)
						f.write(recv_mesg)
						recv_len += len(recv_mesg)
					else:
						# 需要传输的文件数据小于最大传输数据大小
						recv_mesg = clientSock.recv(filesize_b - recv_len)
						recv_len += len(recv_mesg)
						f.write(recv_mesg)
						f.close()
						print("文件接收完毕！")
				# 向用户发送信号，文件已经上传完毕
				completed = "1"
				clientSock.send(bytes(completed, "utf-8"))
				clientSock.close()
				break
			break
		sever.close()

class File_Client(Thread):

	def __init__(self, name, ip, openPort,ipToConnect,portToConnect):
		super().__init__()
		self.openPort = openPort
		self.ipToConnect = ipToConnect
		self.portToConnect = portToConnect
		self.name = name
		self.ip = ip

	def run(self):
		Thread(target=self.client).start()


	def client(self):
		# 创建客户端
		client = socket(AF_INET, SOCK_STREAM)
		ip_port = (self.ipToConnect, 5353)
		buffSize = 1024
		client.connect(ip_port)
		print("connecting...")
		# 开始通信
		while True:
			# 上传文件
			fileInfor = self.name
			num = fileInfor.rfind('\\')
			fileName = fileInfor[num+1:]
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
			client.close()
			break


# if __name__ == '__main__':
#    sev = File_Server(5353,"192.168.43.242",5353)
#    sev.start()
#    clt = File_Client(r"C:\Users\TangZH\Desktop\check\readme.md","192.168.43.242",5353,"192.168.43.20",5353)
#    clt.start()