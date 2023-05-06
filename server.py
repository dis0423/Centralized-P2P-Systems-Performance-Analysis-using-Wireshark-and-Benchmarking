import socket
import threading
from collections import defaultdict

class Server:
    def __init__(self, host='', port=7734, version='1.0'):
        self.host = host
        self.port = port
        self.version = version
        self.peers = defaultdict(set)
        self.files = {}
        self.lock = threading.Lock()

    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print(f'Server {self.version} is listening on port {self.port}')

            while True:
                soc, addr = self.socket.accept()
                print(f'{addr[0]}:{addr[1]} connected')
                thread = threading.Thread(target=self.handler, args=(soc, addr))
                thread.start()
        except KeyboardInterrupt:
            print('\nShutting down the server..\nGood Bye!')
            sys.exit(0)

    def handler(self, soc, addr):
        host = None
        port = None
        while True:
            try:
                req = soc.recv(1024).decode()
                print(f'Receive request:\n{req}')
                lines = req.splitlines()
                version = lines[0].split()[-1]
                if version != self.version:
                    soc.sendall(str.encode(f'{self.version} Version Not Supported\n'))
                else:
                    method = lines[0].split()[0]
                    if method == 'ADD':
                        host = lines[1].split(None, 1)[1]
                        port = int(lines[2].split(None, 1)[1])
                        name = lines[0].split()[-2]
                        self.add_record(soc, (host, port), name)
                    elif method == 'LOOKUP':
                        name = lines[0].split()[-2]
                        self.get_peers_of_files(soc, name)
                    elif method == 'LIST':
                        self.get_all_records(soc)
                    else:
                        raise AttributeError('Method Not Match')
            except ConnectionError:
                print(f'{addr[0]}:{addr[1]} left')
                if host and port:
                    self.clear(host,port)
                soc.close()
                break
            except BaseException:
                try:
                    soc.sendall(str.encode(f'{self.version} 400 Bad Request\n'))
                except ConnectionError:
                    print(f'{addr[0]}:{addr[1]} left')
                    if host and port:
                        self.clear(host,port)
                    soc.close()
                    break

    def clear(self, host, port):
        with self.lock:
            names = self.peers[(host, port)]
            for name in names:
                self.files[name].discard((host, port))
            if not self.files[name]:
                del self.files[name]
            del self.peers[(host, port)]

    def add_record(self, soc, peer, name):
        with self.lock:
            self.peers[peer].add(name)
            if name not in self.files:
                self.files[name] = set()
            self.files[name].add(peer)

        header = f'{self.version} 200 OK\n'
        header += f'files {name} {peer[0]} {peer[1]}\n'
        soc.sendall(str.encode(header))

    def get_peers_of_files(self, soc, name):
        with self.lock:
            if name not in self.files:
                header = f'{self.version} 404 Not Found\n'
            else:
                header = f'{self.version} 200 OK\n'
                for peer in list(self.files[name]):
                    header += f'files {name} {peer[0]} {peer[1]}\n'
        soc.sendall(str.encode(header))

    def get_all_records(self, soc):
        with self.lock:
            if not self.files:
                header = f'{self.version} 404 Not Found\n'
            else:
                header = f'{self.version} 200 OK\n'
                for name in self.files:
                    for peer in list(self.files[name]):
                        header += f'files {name} {peer[0]} {peer[1]}\n'
        soc.sendall(str.encode(header))

if __name__ == '__main__':
    server = Server()
    server.start()