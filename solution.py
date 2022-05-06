import socket
import time
import re

class ClientError(Exception):
    pass

class Client:
    status = ('ok', 'error')
    def __init__(self, host, port, timeout=None):
        self.sock = socket.create_connection((host, port), timeout)

    def get(self, metric):
        self.sock.sendall('get {}\n'.format(metric).encode('utf8'))
        answer = self.sock.recv(1024).decode('utf8').split('\n')
        if answer[0] == 'ok':
            return self.make_dict(answer[1:])
        else:
            raise ClientError


    def put(self, metric, value, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())

        request = 'put {} {} {}\n'.format(metric, value, timestamp)
        self.sock.sendall(request.encode('utf8'))
        answer = self.sock.recv(1024).decode('utf8').split('\n')
        print(answer)
        if not answer[0] == 'ok':
            raise ClientError

    @staticmethod
    def make_dict(array_data):
        dict_data = {}
        # split_data = text_data.split('\n')
        try:
            for string in array_data:
                if string:
                    words = string.split()
                    if not words[0] in dict_data:
                        dict_data[words[0]] = []
                    dict_data[words[0]].append((int(words[2]), float(words[1])))
        except:
            raise ClientError

        for metric in dict_data:
            dict_data[metric] = sorted(dict_data[metric], key=lambda x: x[0])
        
        return dict_data

    def __del__(self):
        self.sock.close()
