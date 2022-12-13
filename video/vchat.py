import pickle
import struct
import time
import zlib
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
        cv2.namedWindow('Remote', cv2.WINDOW_NORMAL)
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
            cv2.imshow('Remote', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                conn.send("Close".encode("utf-8"))
                break



class Video_Client(Thread):
    def __init__(self, ip, port, level, version):
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
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.sock.close()
        self.cap.release()

    def run(self):
        print("VIDEO client starts...")
        Thread(target=self.listening).start()
        while True:
            try:
                self.conn, addr = self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(3)
                continue
        print("VIDEO client connected...")
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
            data = self.conn.recv(1024)
            if data == "Close".encode("utf-8"):
                break
        self.close()

    def close(self):
        self.sock.close()
        self.cap.release()


if __name__ == "__main__":
    Video_Server(9999, 4).start()
    m = Video_Client("192.168.43.20", 9999, 1, 4)
    m.start()

    time.sleep(10)
    m.close()
