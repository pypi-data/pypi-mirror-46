import json
import struct
import os
import socket
from tqdm import tqdm

# todo 中文路径处理
# 空文件夹
class Sender():
    def __init__(self, server_ip):
        self.receiver_ip = server_ip
        self.root_path = '/'
        self.current_progress = 0

    def get_progress(self):
        return self.current_progress  
       
    def _calc_root_of_paths(self, paths):
        if len(paths) == 1:
            self.root_path = os.path.dirname(paths[0])
        else:
            self.root_path = os.path.commonprefix(paths)

    def _send_head(self ,path='/', type='file', is_terminalted=False):         
        head = {
            'relpath': os.path.relpath(path, self.root_path),
            'filesize': os.path.getsize(path),
            'terminated': is_terminalted,
            'type': type  # file or folder
        }
        json_head = json.dumps(head).encode('utf-8')
        # ensure length of head to be exactly 1024
        if len(json_head)<=1024:
            json_head +=(1024-len(json_head))*b' '
        else:
            raise RuntimeError('the head is too long')

        self.sk.send(json_head)
    
    def send(self, files):
        '''
        send files or folder to socket,
        argument should be a list
        '''
        self.sk = socket.socket()
        self.sk.connect(self.receiver_ip)

        self._calc_root_of_paths(files)

        for path in files:
            if os.path.isfile(path):
                self._send_a_file(path)
            elif os.path.isdir(path):
                self._send_a_folder(path)
            else:
                print(path,' is neither a file nor a folder, will be skipped.')

        self._send_head(is_terminalted=True)

        self.sk.close()
        del self.sk


    def _send_a_file(self, file):
        self._send_head(file)
        self._send_content(file)
 
    def _send_content(self, path):
        BUFFER = 1024
        filesize = os.path.getsize(path)

        SIZE = filesize
        with open(path, 'rb') as f:
            print('sending file: ', path)
            with tqdm(total=SIZE) as pbar:
                while filesize:
                    self.current_progress = round((SIZE-filesize)*100/SIZE, 1)
                    # print('r:',filesize)
                    if filesize >= BUFFER:
                        content = f.read(BUFFER)
                        self.sk.send(content)
                        filesize -= BUFFER
                        
                        pbar.update(BUFFER)
                    else:
                        content = f.read(filesize)
                        self.sk.send(content)
                        
                        pbar.update(filesize)
                        break

    def _send_a_folder(self, rootDir):
        for root, dirs, files in os.walk(rootDir):
            self._send_head(path=root, type='folder')
            for file in files:
                file_path = os.path.join(root, file)
                
                assert os.path.isfile(file_path)
                self._send_a_file(file_path)

            for dirname in dirs:
                self._send_a_folder(dirname)


class Receiver():
    def __init__(self):
        self.sk = socket.socket()
        port = 10086
        while True:
            try:
                self.sk.bind(('', port))
                break
            except socket.error as e:
                print('Port:{} is unavailable, change one another.'.format(port))
                port += 1
                continue

        host_ip = socket.gethostbyname('localhost')
        print('receiver is listening on (\'{}\', {})'.format(host_ip, port))
        self.IP = (host_ip, port)
        self.sk.listen(5)

    def get_IP(self):
        return self.IP

    def _recv_exactly_num_bytes(self, conn, NUM):
        content = bytes()
        while len(content) != NUM:
            content += conn.recv(NUM - len(content))
        assert NUM == len(content)
        return content

    def _receive_head(self, conn): 
        head_bytes = self._recv_exactly_num_bytes(conn, 1024)
        head_json = head_bytes.decode('utf-8')
        head = json.loads(head_json)
        return head

    def _mkdir(self, path):
        path = path.strip()
        path = path.rstrip("\\")

        if not os.path.exists(path ):
            os.makedirs(path)
            print(path ,' is created..')
            assert os.path.exists(path), 'path should have been created successfully.'
        else:
            pass
            # print(path ,' is exists.')

    def save_files_to(self, path): 
        file_num = 0
        BUFFER = 1024
        conn, addr = self.sk.accept()
        print('start recving files...')
        while True:
            head = self._receive_head(conn)
            # print(head)
            if head['terminated']:
                break
            else:
                target_path = os.path.join(path, head['relpath'])

                # ensure to have a valid loacal dir path, if not create one.   
                self._mkdir(os.path.dirname(target_path))
                
                if head['type'] == 'file':
                    
                    filesize = head['filesize']
                    SIZE = filesize
                    if os.path.exists(target_path):
                        print(target_path, 'file already exists, will be overwritten.')

                    with open(target_path, 'wb') as f:
                        print('getting file: ', target_path)
                        with tqdm(total=filesize) as pbar:
                            file_num += 1
                            while filesize:
                                # print('t:',filesize)
                                if filesize >= BUFFER:
                                    content = self._recv_exactly_num_bytes(conn, BUFFER)
                                    pbar.update(BUFFER)

                                    filesize -= BUFFER
                                    f.write(content)
                                else:
                                    content = self._recv_exactly_num_bytes(conn, filesize)
                                    pbar.update(filesize)

                                    f.write(content)
                                    break
                    assert os.path.getsize(target_path)==SIZE, 'file is not correctly saved.'

                elif head['type'] == 'folder':
                    pass
        conn.close()
        
        print(file_num, ' files received.')

if __name__ == '__main__':

    import threading
    toPATH = '/Users/vt/Desktop/copyto'

    # files or folders to be sent. list
    files = [
    '/Users/vt/Desktop/TEST/TEST.pdf',
    '/Users/vt/Desktop/TEST/icon',
    '/Users/vt/Desktop/TEST/wonderbit', 
    ]

    rx = Receiver()
    ip = rx.get_IP()

    # sender should be created after receiver creating.
    tx = Sender(ip)

    thread1 = threading.Thread(
        target=lambda: rx.save_files_to(toPATH))

    thread2 = threading.Thread(
        target=lambda: tx.send(files))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()



