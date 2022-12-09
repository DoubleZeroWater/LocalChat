import socket
import os
import sys
import struct
import tarfile
save_path = "E:\\test"
port = ('192.168.31.190',5354)

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        s.bind(port)
        s.listen(2)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('waiting..............')
    while True:
        sock, addr = s.accept()
        deal_data(sock, addr, save_path)
        extent_tar(save_path)

def deal_data(sock, addr, save_path):
    print("Accept from{0}".format(addr))
    while True:
        fileinfo_size = struct.calcsize('128sq')
        buf = sock.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sq', buf)
            fn = filename.decode().strip('\x00')

            file_new_name = os.path.join(save_path, fn)
            print('newname is {0}, filesize {1}'.format(file_new_name,filesize))
            recvd_size = 0
            fp = open(file_new_name, 'wb')
            print('start receving')

            while not recvd_size == filesize:
                if filesize - recvd_size >1024:
                    data = sock.recv(1024)
                    recvd_size += len(data)
                else:
                    data = sock.recv(1024)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            print('Files received')
        sock.close()
        break

def extent_tar(save_path):
    tar_path = os.walk(save_path)
    for path, dir_list, file_list in tar_path:
        for dir_name in file_list:
            tarname = os.path.join(path, dir_name)
            if os.path.splitext(tarname)[-1] == '.tar':
                print('TRUE')
                tar = tarfile.open(tarname, 'r:')
                file_names = tar.getnames()
                for file_name in file_names:
                    tar.extract(file_name, save_path)
                tar.close()
                print('tarfile extented')
                os.remove(tarname)
                print('tarfile deleted')


if __name__ == '__main__':
    socket_service()
