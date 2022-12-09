import socket
import os
import sys
import struct
import tarfile


port = ('192.168.31.190',5354)


def sock_client_image():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(port)
        except socket.error as msg:
            print(msg)
            print(sys.exit(1))
        filespath = input('发送的文件夹路径 ')
        filepath = input('打包路径')
        with tarfile.open(filepath, 'w') as tar:
            tar.add(filespath, arcname=os.path.basename(filespath))
        fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                            os.stat(filepath).st_size)
        s.send(fhead)
        fp = open(filepath, 'rb')
        while True:
            data = fp.read(1024)
            if not data:
                print('{0} send over...'.format(filepath))
                break
            s.send(data)
        fp.close()
        s.close()
        os.remove(filepath)


if __name__ == '__main__':
    sock_client_image()
