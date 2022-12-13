import pickle
import struct
import time
import zlib
from socket import *
from threading import Thread

import cv2

CloseSign = False

class Video_Client(Thread):
    # 视频客户端
    def __init__(self, ip, port, level, version):
        super().__init__()
        self.ADDR = (ip, port)  # 连接地址
        if level <= 3:
            self.interval = level
        else:
            self.interval = 3
        self.fx = 1 / (self.interval + 1)
        if self.fx < 0.3:
            self.fx = 0.3
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.sock.close()
        self.cap.release()

    def close(self):
        global CloseSign
        CloseSign = True
        try:
            if self.sock:
                self.sock.close()
            try:
                self.cap.release()
            except:
                pass
        except:
            pass

    def close_listener(self):
        # 监听服务器发过来的摄像头关闭事件
        while not CloseSign:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                if msg == 'CLOSE_VIDEO_SESSION':
                    print('Receive close request, try to close')
                    self.close()
                    print('Close done')
                    # break
            except:
                self.sock.close()
                self.cap.release()
            finally:
                print('self.cap.isOpened(): ', self.cap.isOpened())
                break

    def run(self):
        global CloseSign
        try:
            print("VIDEO client starts...")
            while not CloseSign:
                # 循环连接，如果连接不上，间隔一秒后再次连接
                try:
                    self.sock.connect(self.ADDR)
                    break
                except:
                    if not CloseSign:
                        return
                    time.sleep(1)
                    # continue
            print("VIDEO client connected...")

            # 同步监听摄像头关闭请求
            cl = Thread(target=self.close_listener)
            cl.start()

            while self.cap.isOpened() and not CloseSign and not CloseSign:
                ret, frame = self.cap.read()
                # 一个矩形窗口，即相机所拍摄的窗口大小
                sframe = cv2.resize(frame, (1280, 720), fx=self.fx, fy=self.fx)
                data = pickle.dumps(sframe)
                zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
                try:
                    # 将图像数据压缩后发送到服务端
                    self.sock.sendall(struct.pack("L", len(zdata)) + zdata)
                except:
                    break
                for i in range(self.interval):
                    self.cap.read()
        except:
            pass


class Video_Server(Thread):
    # 服务器端最终代码如下，增加了对接收到数据的解压缩处理。
    # 服务器是用来接收Client发送的图像数据并且显示的
    def __init__(self, port, version):
        super().__init__()
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

    def close(self):
        global CloseSign
        CloseSign = True
        try:
            if self.conn:
                self.conn.send(bytes('CLOSE_VIDEO_SESSION', encoding='utf-8'))
            if self.sock:
                self.sock.close()
            try:
                time.sleep(1)
                cv2.destroyAllWindows()
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    def run(self):
        global CloseSign
        try:
            print("VEDIO server starts...")
            self.sock.bind(self.ADDR)
            self.sock.listen(60)
            print('Server started, waiting for connection...')
            self.conn, addr = self.sock.accept()
            print("remote VEDIO client success connected...")
            data = "".encode("utf-8")
            payload_size = struct.calcsize("L")
            winname = 'VChat'
            cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
            while not CloseSign:
                while len(data) < payload_size and not CloseSign:
                    data += self.conn.recv(81920)
                    print("Doing while")
                packed_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("L", packed_size)[0]
                while len(data) < msg_size:
                    data += self.conn.recv(81920)
                zframe_data = data[:msg_size]
                data = data[msg_size:]
                frame_data = zlib.decompress(zframe_data)
                frame = pickle.loads(frame_data)
                cv2.imshow(winname, frame)
                # 通过按Esc或者点击x可以关闭窗口
                keyCode = cv2.waitKey(1)
                prop = cv2.getWindowProperty(winname, cv2.WND_PROP_AUTOSIZE)
                if keyCode != -1 or prop == -1:
                    # 退出后，向Client发送一个关闭信号
                    try:
                        print("I tell you.")
                        self.conn.send(bytes('CLOSE_VIDEO_SESSION', encoding='utf-8'))
                        self.close()
                    except:
                        print('Try to tell client close, but failed')
                    finally:
                        self.conn.close()
                        break
            print("Out of while")
        except Exception as e:
            print(e)
            self.close()


if __name__ == "__main__":
    # This is the demo to test the video chat file
    vServer = Video_Server(5556, 4)
    vServer.start()
    vClient = Video_Client('127.0.0.1', 5556, 1, 4)
    vClient.start()

    time.sleep(5)
    vServer.close()
