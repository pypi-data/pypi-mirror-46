import json
import struct
import os
import socket

class Receiver():
    def __init__(self):
        self.sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        port = 10086
        while True:
            try:
                self.sk.bind( ('', port) )
                break
            except socket.error as e:
                print('Port:{} is unavailable, change one another.'.format(self.port))
                port +=1
                continue

        host_ip = socket.gethostbyname(socket.gethostname())
        print('receiver is listening on (\'{}\', {})'.format(host_ip, port))        
        self.IP = (host_ip, port)

    def get_IP(self):
        return self.IP

    def _mkdir(self, path):
        path=path.strip()
        path=path.rstrip("\\")
        if os.path.exists(path):
            print(path+' path already exists.')
            return False
        else:
            os.makedirs(path) 
            print(path+' dir created.')
            return True

    def receive_files_to(self,to_path):
        self.sk.listen(1)
        source_root = '/'
        BUFFER = 1024
        conn, addr = self.sk.accept()
        while True:
            pack_len = conn.recv(4)
            head_len = struct.unpack('i', pack_len)[0]
            json_head = conn.recv(head_len).decode('utf-8')
            head = json.loads(json_head)
            
            target_path = os.path.join(to_path ,head['relpath'])
            
            if head['terminated']:
                break
            if head['type'] == 'folder':
                self._mkdir( target_path )
            elif head['type'] == 'file':
                with open(target_path, 'wb') as f:
                    filesize = head['filesize']
                    while filesize:
                        # print('t:',filesize)
                        if filesize >= BUFFER:
                            content = conn.recv(BUFFER)
                            filesize -= BUFFER
                            f.write(content)
                        else:
                            content = conn.recv(filesize)
                            f.write(content)
                            break
        conn.close()
        self.close_socket()

    def close_socket(self):
        self.sk.close()

class Sender():
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.root_path = '/'
    
    def connect_socket(self):
        self.sk.connect(self.server_ip)

    def _send_head_of_file(self,path='/', type='file', is_terminalted=False):
        head = {
            'relpath':os.path.relpath(path, self.root_path),
            'filesize': os.path.getsize(path),
            'terminated':is_terminalted,
            'type':type # file or folder
        }
        bytes_head = json.dumps(head).encode('utf-8')
        head_len = len(bytes_head)
        pack_len = struct.pack('i', head_len)

        self.sk.send(pack_len)  # 先发报头长度
        self.sk.send(bytes_head)  # 再发送byte类型的报头

    def _send_a_file(self, path):
        BUFFER = 1024
        self._send_head_of_file(path)

        filesize = os.path.getsize(path)
        with open(path, 'rb') as f:
            while filesize:
                # print('r:',filesize)
                if filesize >= BUFFER:
                    content = f.read(BUFFER)  # 每次读出来的内容
                    self.sk.send(content)
                    filesize -= BUFFER
                else:
                    content = f.read(filesize)
                    self.sk.send(content)
                    break
    def _send_a_folder(self, rootDir):
        #遍历根目录
        for root,dirs,files in os.walk(rootDir):
            self._send_head_of_file(path=root, type='folder')
            for file in files:
                file_path = os.path.join(root,file)

                if os.path.isfile(file_path):
                    self._send_a_file(file_path)
                else:
                    pass
            for dirname in dirs:
                #递归调用自身,只改变目录名称
                self._send_a_folder(dirname)

    def transfer_files_or_folders(self, paths):
        self.root_path = os.path.commonprefix(paths)
        self.connect_socket()
        for path in paths:
            if os.path.isfile(path):
                self._send_a_file(path)
            elif os.path.isdir(path):
                self._send_a_folder(path)
        self.close_socket()

    def close_socket(self):
        self._send_head_of_file(is_terminalted=True)
        self.sk.close()

if __name__ == '__main__':   
    
    import threading
    toPATH = '/Users/vt/Desktop/copyto'   
    # files or folders to be sent. list 
    files = ['/Users/vt/Desktop/icon', '/Users/vt/Desktop/TEST.pdf']     
    
    r = Receiver()  
    ip = r.get_IP()

    # sender should be created after receiver creating.
    t = Sender(ip)

    thread1 = threading.Thread(
        target=lambda :r.receive_files_to(toPATH) )

    thread2 = threading.Thread(
        target=lambda :t.transfer_files_or_folders(files))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()