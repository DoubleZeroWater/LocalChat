import pickle
import struct
import time
import zlib
from random import randint
from socket import *
from threading import Thread

import cv2

CloseSign = False

class Video_Server(Thread):
    def __init__(self, port, version):
        global CloseSign
        CloseSign = False
        Thread.__init__(self)
        self.ADDR = ('', port)
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)

    def __del__(self):
        self.sock.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass

    def run(self):
        global CloseSign
        print("VIDEO server starts...")
        self.sock.bind(self.ADDR)
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        print("remote VIDEO client success connected...")
        data = "".encode("utf-8")
        payload_size = struct.calcsize("L")  # 结果为4
        title = str(randint(0, 100))
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        while True:
            while len(data) < payload_size:
                data += conn.recv(81920)
            packed_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_size)[0]
            while len(data) < msg_size:
                data += conn.recv(81920)
            zframe_data = data[:msg_size]
            data = data[msg_size:]
            frame_data = zlib.decompress(zframe_data)
            frame = pickle.loads(frame_data)
            cv2.imshow(title, frame)
            if cv2.waitKey(1) & 0xFF == 27:
                conn.send("Close".encode("utf-8"))
                break



class Video_Client(Thread):
    def __init__(self, ip, port, level, version):
        self.conn = None
        global CloseSign
        CloseSign = False
        Thread.__init__(self)
        self.ADDR = (ip, port)
        if level <= 3:
            self.interval = level
        else:
            self.interval = 3
        self.fx = 1 / (self.interval + 1)
        if self.fx < 0.3:  # 限制最大帧间隔为3帧
            self.fx = 0.3
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        self.sock.close()
        self.cap.release()

    def run(self):
        print("VIDEO client starts...")
        while True:
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(3)
                continue
        print("VIDEO client connected...")
        time.sleep(2)
        Thread(target=self.listening).start()
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            sframe = cv2.resize(frame, (0, 0), fx=self.fx, fy=self.fx)
            data = pickle.dumps(sframe)
            zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            try:
                self.sock.sendall(struct.pack("L", len(zdata)) + zdata)
            except:
                break
            for i in range(self.interval):
                self.cap.read()

    def listening(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data.decode("utf-8") == "Close":
                    break
            except Exception as e:
                print(e)
        self.close()

    def close(self):
        self.sock.close()
        self.cap.release()


if __name__ == "__main__":
    Video_Server(9999, 4).start()
    Video_Client("192.168.251.190", 9999, 1, 4).start()
    time.sleep(20)
    Video_Server(9999, 4).start()
    Video_Client("192.168.251.190", 9999, 1, 4).start()
