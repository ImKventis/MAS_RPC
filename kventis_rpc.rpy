
# Submod made with love by u/KventisAndM
# https://github.com/ImKventis


init -990 python in mas_submod_utils:
    Submod(
        author="Kventis",
        name="Discord RPC",
        description="A discord rich pressence client for monika",
        version="1.0.0",
        dependencies={},
        settings_pane="kventis_rpc_setting_pane",
        version_updates={}
    )
init python in kventis_rpc:
    # JSON RPC for Discord
    from abc import abstractmethod
    import socket
    import os
    import platform
    import time
    import store


    def log(msg_type, msg):
        if msg_type == "info":
            store.mas_submod_utils.submod_log.info("[Discord RPC] " + msg)
        elif msg_type == "warn":
            store.mas_submod_utils.submod_log.warning("[Discord RPC] " + msg)
        else:
            store.mas_submod_utils.submod_log.error("[Discord RPC] " + msg)

    dis_client_id = '977282947981910026'
    client = None
    custom_rpc_file_path = os.path.join(renpy.config.basedir, "./custom_presense.txt")
    custom_rpc_file = None
    special_queue = []
    
    #Store
    # store.persistent.rpc_enabled = store.persistent.rpc_enabled
    # store.persistent.rpc_use_custom = store.persistent.rpc_use_custom
    # store.persistent.rpc_first = store.persistent.rpc_first

    if store.persistent.rpc_enabled is None:
        store.persistent.rpc_enabled = True
    
    if store.persistent.rpc_use_custom is None:
        store.persistent.rpc_use_custom = False

    print store.persistent.rpc_first 
    print store.persistent.rpc_first is None
    if store.persistent.rpc_first is None:
        store.persistent.rpc_enabled = False

    start_time = int(time.time())
    default_act = {
        'details': 'Spending time with ',
        # 'state': 'In the spaceroom',
        'timestamps': {
            'start': start_time
        },
        'assets': {
            'large_text': 'Monika After Story',
            'large_image': 'maslogo',
        }
    }
    loading_act = {
        'details': 'Waiting for RPC...',
        'timestamps': {
            'start': start_time
        },
        'assets': {
            'large_text': 'Monika After Story',
            'large_image': 'maslogo',
        }
    }

    class RPC_Event(object):
        def __init__(self, content, ticks):
            self.content = content
            self.ticks = ticks

        def tick(self):
            self.ticks = self.ticks - 1

    class DiscordClientUni(object):
        def __init__(self):
            self.s_sock = None
            self.connected = False

        def start(self):
            self.connected = self.reconnect()
            if self.connected:
                try:
                    self.handshake()
                except RuntimeError as e:
                    log("warn", "Handshake failed: " + str(e))
                    self.connected = False

        @abstractmethod
        def connect(self):
            pass

        @abstractmethod
        def receive(self, size):
            pass

        @abstractmethod
        def write(self, data):
            pass

        def close(self):
            if self.connected == False:
                return
            try:
                self.send({}, 2)
            finally:
                self.s_sock.close()
                self.connected = False

        def reconnect(self):
            try:
                self.close()
            except:
                # Probs gonna fail
                pass
            status = self.connect()
            if self.connected:
                self.handshake()
            return status

        def send_read(self, data, op=1):
            self.send(data, op)
            return self.read()

        def handshake(self):
            ret_op, ret_data = self.send_read({'v': 1, 'client_id': dis_client_id}, op=0)
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

        def ping(self):
            return self.send_read({"msg": "pong"}, 3)

    class DiscordClientUnix(DiscordClientUni):

        def __init__(self):
            self.s_sock = None
            self.connected = False

        def start(self):
            self.connected = self.reconnect()
            if self.connected:
                try:
                    self.handshake()
                except RuntimeError as e:
                    log("warn", "Handshake failed: " + str(e))
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
            # Wouldnt boot forever otherwise
            self.s_sock.settimeout(3)
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

        def receive(self, size):
            return self.s_sock.recv(size)

        def write(self, data):
            self.s_sock.sendall(data)
 
    class DiscordClientWin(DiscordClientUni):
        def __init__(self):
            self.s_sock = None
            self.connected = False

        def start(self):
            self.connected = self.connect()
            if self.connected:
                try:
                    self.handshake()
                except RuntimeError as e:
                    log("warn", "Handshake failed: " + str(e))
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

        def receive(self, size):
            return self.s_sock.read(size)

        def write(self, data):
            self.s_sock.write(data)
            self.s_sock.flush()

    def add_rpc_event(content, ticks):
        rpc_event = RPC_Event(content, ticks)
        special_queue.append(rpc_event)

    def gen_client():
        # Unix 💪
        if platform.platform() == 'Windows':
            return DiscordClientWin()
        else:
            return DiscordClientUnix() 

    def toggle_rpc():
        if store.persistent.rpc_enabled:
            store.persistent.rpc_enabled = False

            try:
                client.close()
            except Exception as e:
                log('warn', 'Failed to close.: ' + str(e))

            log('info', 'RPC Disabled')

            store.mas_submod_utils.unregisterFunction(
                "ch30_minute",
                update_activity
            )

            store.mas_submod_utils.unregisterFunction("quit", client.close)

        else:
            store.persistent.rpc_enabled = True
            try:
                client.start()
            except Exception as e:
                log('error', "Failed to start client " + str(e))
            log('info', 'RPC Enabled')

            if client.connected:
                update_activity(client)


            store.mas_submod_utils.registerFunction(
                "ch30_minute",
                update_activity,
                args=[client]
            )

            store.mas_submod_utils.registerFunction("quit", client.close)

    def update_activity(client):
        ping = None
        # Ping RPC server to check connection is still alive
        try:
            ping = client.ping()
            # log('info', 'Ping: ok')
            # Pings every minute uneeded logging
        except:
            pass

        # Ping failed so reconnect
        if ping == None:
            try:
                client.reconnect()
            except:
                # Failed to reconnect try again in a minute and dont bother setting activity
                return

        new_act = dict(default_act)
        new_act['details'] = new_act['details'] + store.m_name

        # special events usually timed.  
        if len(special_queue) > 0:
            new_act.update({'state': special_queue[0].content})
            special_queue[0].tick()
            if special_queue[0].ticks <= 0:
                special_queue.pop(0)

        elif store.persistent.rpc_use_custom and custom_rpc_file != 'auto':
            new_act['state'] = custom_rpc_file

        try:
            client.activity(new_act)
        except:
            log('warn', 'Failed to set activity: ' + str(e))

    def update_custom():
        global custom_rpc_file
        if os.path.exists(custom_rpc_file_path):
            with open(custom_rpc_file_path, "r") as f:
                custom_rpc_file = f.read()
                f.close()
            if len(custom_rpc_file) == 0:
                store.persistent.rpc_use_custom = False
                log("warn", "Custom RPC file is empty, disabling custom RPC")
            elif len(custom_rpc_file) > 200:
                store.persistent.rpc_use_custom = False
                log("warn", "Custom RPC file is too long, disabling custom RPC")
        else:
            log("info", "Custom RPC file not found, creating default")
            with open(custom_rpc_file_path, "w+") as f:
                f.write("auto")
                f.close

    client = gen_client()

    if store.persistent.rpc_enabled:
        client.start()

        try:
            client.activity(loading_act)
        except Exception as e:
            log('warn', 'Failed to set activity: ' + str(e))

        store.mas_submod_utils.registerFunction(
            "ch30_minute",
            update_activity,
            args=[client]
        )

        store.mas_submod_utils.registerFunction("quit", client.close)

    if store.persistent.rpc_use_custom:
        update_custom()


# Runs once when first installed
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="kventis_rpc_installed",
            conditional="True",
            action=EV_ACT_QUEUE,
        )
    )

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="kventis_rpc_installed_talk",
            prompt="Can you tell me about RPC?",
            category=['dev'],
            pool=True,
            unlocked=True,
        ),
        markSeen=False
)

label kventis_rpc_installed_talk:
    call kventis_rpc_installed
    return


label kventis_rpc_installed:
    $ import store
    m "[player], I see you added some .rpy files"
    m "Let's have a look inside.{w=0.3}.{w=0.3}."
    m "Oh a RPC client for discord!"
    m "Thanks, [player]!"
    m "Should I connect now?{nw}"
    $ _history_list.pop()
    $ menu_res = False
    menu:
        m "Should I connect now?{fast}"
        "Yes.":
            $ menu_res = True
        "No.":
            # Jump to beginning
            pass
    
    if menu_res:
        m "Connecting now..."
        $ kventis_rpc.toggle_rpc()
        $ kventis_rpc.add_rpc_event("Hey everyone! - Monika", 3)
        m "RPC is ready to go!"
        m "I even added a little message for 3 minutes!"
    else:
        m "Oh okay."
        m "You can enable it from the \"SubMods\" menu."

    m "Thanks for this again."
    $ store.persistent.rpc_first = False
    return