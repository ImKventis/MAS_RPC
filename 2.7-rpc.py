from abc import abstractmethod
import socket
import os
import platform
import time

client_id = '977282947981910026'

# Huge help from https://github.com/JellyWX/python-discord-rpc
# Lib orignally made for Python 3.7 
# I have had to make some changes to the classes for it to even work at all with Python 2.7


class DiscordClientUni(object):
    def __init__(self):
        self.s_sock = None
        self.connected = self.connect()
        if self.connected:
            try:
                self.handshake()
            except RuntimeError as e:
                print(e)
                self.connected = False

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def receive(self, size):
        pass

    @abstractmethod
    def write(self, data):
        pass

    def reconnect(self):
        try:
            self.close()
        except:
            # Probs gonna fail
            pass
        self.connected = self.connect()
        if self.connected:
            self.handshake()
        return

    def send_read(self, data, op=1):
        self.send(data, op)
        return self.read()

    def handshake(self):
        ret_op, ret_data = self.send_read({'v': 1, 'client_id': client_id}, op=0)
        if ret_op == 1 and ret_data['cmd'] == 'DISPATCH' and ret_data['evt'] == 'READY':
            return
        else:
            if ret_op == 2:
                self.close()
            raise RuntimeError(ret_data)   

    def send(self, data, op=1):
        import json
        import struct
        to_send = json.dumps(data, separators=(',', ':')).encode('utf-8')
        header = struct.pack("<II", op, len(to_send))
        self.write(header)
        self.write(to_send)

    def read_data(self, size):
        buffer = b""
        left = size
        while left:
            chunk = self.receive(size)
            buffer += chunk
            left -= len(chunk)
        return buffer
 
    def read_header(self):
        import struct
        header = self.read_data(8)
        return struct.unpack("<II", header)

    def read(self):
        import json
        op, leng = self.read_header()
        data_str = self.read_data(leng)
        return op, json.loads(data_str.decode('utf-8'))

    def activity(self, activity):
        import uuid
        self.send({
            'cmd': 'SET_ACTIVITY',
            'args': {  
                'pid': os.getpid(),
                'activity': activity
            },
            'nonce': str(uuid.uuid4())
        }) 

    def update_activity(self):
        # Run checks to update activity
        pass

    def ping(self):
        return Client.send_read({"msg": "pong"}, 3)

class DiscordClientUnix(DiscordClientUni):

    def __init__(self):
        self.s_sock = None
        self.connected = self.connect()
        if self.connected:
            try:
                self.handshake()
            except RuntimeError as e:
                print(e)
                self.connected = False

    def connect(self):
        main_keys = ('XDG_RUNTIME_DIR', 'TMPDIR', 'TMP', 'TEMP')
        for key in main_keys:
            pos_path = os.environ.get(key)
            if pos_path:
                break
        else:
            pos_path = '/tmp'
        pos_path = os.path.join(pos_path, 'discord-ipc-{}')
        # kventis_rpc.
        self.s_sock = socket.socket(socket.AF_UNIX)
        for i in range(10):
            path = pos_path.format(i)
            if os.path.exists(path):
                try:
                    # kventis_rpc.
                    self.s_sock.connect(path)
                except OSError as e:
                    pass
                except:
                    return False
                else:
                    return True
        else:
            return False

    def close(self):
        self.s_sock.close()
        self.connected = False

    def receive(self, size):
        return self.s_sock.recv(size)

    def write(self, data):
        self.s_sock.sendall(data)
        
# Win10 is weird its just a file?
# I dont use windows so I'm unsure if this works yet
# Needs testing in a VM  
class DiscordClientWin(DiscordClientUni):
    def __init__(self):
        self.s_sock = None
        self.connected = self.connect()
        if self.connected:
            try:
                self.handshake()
            except RuntimeError as e:
                print(e)
                self.connected = False

    def connect(self):
        # What the duck
        main_path = R'\\?\pipe\discord-ipc-{}'
        for i in range(10):
            pos_path = main_path.format(i)
            try: 
                self._s_sock = open(pos_path, "w+b")
            except:
                # Didnt find path that sucks
                pass
            else:
                # Found a path that works thats cool
                return True
        else:
            # Cringe tbh
            return False

    def close(self):
        self.s_sock.close()
        self.connected = False

    def receive(self, size):
        return self.s_sock.read(size)

    def write(self, data):
        self.s_sock.write(data)
        self.s_sock.flush()


start = int(time.time())
default_act = {
    'details': 'Spending time with Monika',
    #'state': 'In the spaceroom',
    'timestamps': {
        'start': start
    },
    'assets': {
        'large_text': 'Monika After Story',
        'large_image': 'maslogo',
    }
}



Client = DiscordClientUnix()
Client.activity(default_act)

# ch30-loop basically
while True:
    ping = None
    # Ping RPC server to check connection is still alive
    try:
        ping = Client.ping()
        print(ping)
    except:
        pass

    # Ping failed so reconnect
    if ping == None:
        try:
            Client.reconnect()
        except:
            # Failed to reconnect try again in a minute
            pass
    time.sleep(60)
