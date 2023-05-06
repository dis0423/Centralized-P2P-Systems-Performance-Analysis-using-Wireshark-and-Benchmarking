
import socket
import threading
from pathlib import Path
import platform
import mimetypes
import os
import sys
import time
import random
NUMBER_files=2
class MyException(Exception):
    pass

class Client:
    def __init__(self, server_host='localhost', version='1.0', directory='files'):
        self.server_host = server_host
        self.server_port = 7734
        self.version = version
        self.directory = directory
        Path(self.directory).mkdir(exist_ok=True)
        self.upload_port = None
        self.shareable = True

    def start(self):
        print(f'Connecting to the server {self.server_host}:{self.server_port}')
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.connect((self.server_host, self.server_port))
        except Exception:
            print('Server Not Available.')
            return

        print('Connected')
        uploader_process = threading.Thread(target=self.init_upload)
        uploader_process.start()
        while self.upload_port is None:
            pass
        print(f'Listening on the upload port {self.upload_port}')
        print(f'Listening on the port {self.server.getsockname()[1]}')
        self.cli()

    def cli(self):
        command_dict = {
            '1': self.add,
            '2': self.lookup,
            '3': self.list_all,
            '4': self.pre_download,
            '5': self.shutdown,
            '6': self.benchmark_filec,
            '7': self.benchmark_filetrans
        }
        while True:
            req = input('\n1: Add, 2: Look Up, 3: List All, 4: Download, 5: Shut Down, 6:Bench_FC, 7:Bench_FT\nEnter your request: ')
            command_dict.setdefault(req, self.invalid_input)()

    def init_upload(self):
        self.uploader = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.uploader.bind(('', 0))
        self.upload_port = self.uploader.getsockname()[1]
        self.uploader.listen(5)

        while self.shareable:
            requester, addr = self.uploader.accept()
            handler = threading.Thread(target=self.handle_upload, args=(requester, addr))
            handler.start()
        self.uploader.close()

    def handle_upload(self, soc, addr):
        header = soc.recv(1024).decode().splitlines()
        try:
            version = header[0].split()[-1]
            name = header[0].split()[-2]
            method = header[0].split()[0]
            path = f'{self.directory}/{name}'
            if version != self.version:
                soc.sendall(str.encode(f'{self.version} Version Not Supported\n'))
            elif not Path(path).is_file():
                soc.sendall(str.encode(f'{self.version} 404 Not Found\n'))
            elif method == 'GET':
                header = f'{self.version} 200 OK\n'
                header += f'Data: {time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())}\n'
                header += f'OS: {platform.platform()}\n'
                header += f'Last-Modified: {time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(os.path.getmtime(path)))}\n'
                header += f'Content-Length: {os.path.getsize(path)}\n'
                header += f'Content-Type: {mimetypes.MimeTypes().guess_type(path)[0]}\n'
                soc.sendall(header.encode())
                try:
                    print('\nUploading...')
                    send_length = 0
                    with open(path, 'r') as file:
                        to_send = file.read(1024)
                        while to_send:
                            send_length += len(to_send.encode())
                            soc.sendall(to_send.encode())
                            to_send = file.read(1024)
                except Exception:
                    raise MyException('Uploading Failed')
                print('Uploading Completed.')
                print('\n1: Add, 2: Look Up, 3: List All, 4: Download\nEnter your request: ')
            else:
                raise MyException('Bad Request.')
        except Exception:
            soc.sendall(str.encode(f'{self.version} 400 Bad Request\n'))
        finally:
            soc.close()

    def add(self, name=None):
        if not name:
            name = input('Enter the file name: ')
        
        file_path = Path(f'{self.directory}/{name}')
        
        if not file_path.is_file():
            raise MyException('File does not exist!')
        
        msg = f'ADD file {name} {self.version}\n'
        msg += f'Host: {socket.gethostname()}\n'
        msg += f'Port: {self.upload_port}\n'
    
        self.server.sendall(msg.encode())
        res = self.server.recv(1024).decode()
        print(f'Receive response: \n{res}')

    def lookup(self, name=None):
        if name is None:
            name = input('Enter the file name ')
        
        msg = f'LOOKUP files {name} {self.version}\n'
        msg += f'Host: {socket.gethostname()}\n'
        msg += f'Port: {self.upload_port}\n'
        
        self.server.sendall(msg.encode())
        res = self.server.recv(1024).decode()
        print(f'Receive response: \n{res}')

    def list_all(self):
        msg = f'LIST ALL {self.version}\n'
        msg += f'Host: {socket.gethostname()}\n'
        msg += f'Post: {self.upload_port}\n'
        
        self.server.sendall(msg.encode())
        res = self.server.recv(1024).decode()
        print(f'Receive response: \n{res}')

    def pre_download(self, file=None, name=None):
        if name == None:
            name = input('Enter the file name')
        
        msg = f'LOOKUP file {name} {self.version}\n'
        msg += f'Host: {socket.gethostname()}\n'
        msg += f'Post: {self.upload_port}\n'
        
        self.server.sendall(msg.encode())
        
        lines = self.server.recv(1024).decode().splitlines()
        
        if lines[0].split()[1] == '200':
            print('Available peers: ')
            for i, line in enumerate(lines[1:]):
                line = line.split()
                print(f'{i + 1}: {line[-2]}:{line[-1]}')

            try:
                no_of_peers= len(lines) -1
                idx=random.randint(1,no_of_peers)
                print("Using random call choosing peer ",idx," to download")
                peer_host = lines[idx].split()[-2]
                peer_port = int(lines[idx].split()[-1])
            except Exception:
                raise MyException('Invalid Input.')
            
            if((peer_host, peer_port) == (socket.gethostname(), self.upload_port)):
                raise MyException('Do not choose yourself.')
            
            self.download(name , peer_host, peer_port)
        
        elif lines[0].split()[1] == '400':
            raise MyException('Invalid Input.')
        
        elif lines[0].split()[1] == '404':
            raise MyException('File Not Available.')
        
        elif lines[0].split()[1] == '500':
            raise MyException('Version Not Supported.')

    def download(self, name, peer_host, peer_port):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            if soc.connect_ex((peer_host, peer_port)):
                raise MyException('Peer Not Available')
            
            msg = f'GET file {name} {self.version}\n'
            msg += f'Host: {socket.gethostname()}\n'
            msg += f'OS: {platform.platform()}\n'
            
            soc.sendall(msg.encode())

            header = soc.recv(1024).decode()
            
            print(f'Receive response header: \n{header}')
            
            header = header.splitlines()
            
            if header[0].split()[-2] == '200':
                path = f'{self.directory}/{name}'
                
                print('Downloading...')
                
                try:
                    with open(path, 'w') as file:
                        content = soc.recv(1024)
                        while content:
                            file.write(content.decode())
                            content = soc.recv(1024)
                except Exception:
                    raise MyException('Downloading Failed')

                total_length = int(header[4].split()[1])

                if os.path.getsize(path) < total_length:
                    raise MyException('Downloading Failed')

                print('Downloading Completed.')
                
                print('Sending ADD request to share...')
                
                if self.shareable:
                    self.add(name)
            
            elif header[0].split()[1] == '400':
                raise MyException('Invalid Input.')
            
            elif header[0].split()[1] == '404':
                raise MyException('File Not Available.')
            
            elif header[0].split()[1] == '500':
                raise MyException('Version Not Supported.')
        finally:
            soc.close()

    def invalid_input(self):
        raise MyException('Invalid Input.')

    def shutdown(self):
        print('\nShutting Down...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    
    def benchmark_filec(self):
        print("started to create files\n")
        start=time.process_time()
        file_size=2
        for i in range (NUMBER_files):
            print("creating file of size ",file_size," bytes\n")
            file_name="files/file"+str(file_size)+".txt"
            with open(file_name, 'wb') as f:
                f.seek(file_size)
                f.write('0'.encode())
            file_size=file_size*2
        print("finished creating fies in ",time.process_time()-start," ms\n")
        print("adding files...\n")
        start=time.process_time()
        file_size=2
        for i in range (NUMBER_files):
            self.add(name="file"+str(file_size)+".txt")
            file_size=file_size*2
        print("finished ADDING files in ",time.process_time()-start," ms\n")
        print("LookUp FIles files...\n")
        start=time.process_time()
        file_size=2
        for i in range (NUMBER_files):
            self.lookup(name="file"+str(file_size)+".txt")
            file_size=file_size*2
        print("finished Looking Up s files in ",time.process_time()-start," ms\n")

    def benchmark_filetrans(self):
        start=time.process_time()
     
        file_size=2
        for i in range (NUMBER_files):
            self.pre_download(name="file"+str(file_size)+".txt")
            file_size=file_size*2
        print("finished DOWNLOADING FILES files in ",time.process_time()-start," ms\n")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        client = Client(sys.argv[1])
    else:
        client = Client()
    client.start()
