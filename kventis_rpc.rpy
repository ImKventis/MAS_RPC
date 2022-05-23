
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

    client_id = '977282947981910026'
    client = None
    rpc_base = os.path.join(renpy.config.basedir, "./rpc/")
    custom_rpc_file_path = os.path.join(rpc_base, "custom_presense.txt")
    custom_rpc_file = None
    rpc_last_brb = None
    rpc_last_brb_label = None
    
    #Store
    # store.persistent.rpc_enabled = store.persistent.rpc_enabled
    # store.persistent.rpc_use_custom = store.persistent.rpc_use_custom
    # store.persistent.rpc_first = store.persistent.rpc_first

    if store.persistent.rpc_enabled is None:
        store.persistent.rpc_enabled = True
    
    if store.persistent.rpc_use_custom is None:
        store.persistent.rpc_use_custom = False

    if store.persistent.rpc_use_brb_status is None:
        store.persistent.rpc_use_brb_status = True

    if store.persistent.rpc_use_room_status is None:
        store.persistent.rpc_use_room_status = True

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
    # loads when ch30-minute hasnt been updated yet
    loading_act = {
        'details': 'Waiting for RPC...',
        'state': 'waiting for next ch30_minute',
        'timestamps': {
            'start': start_time
        },
        'assets': {
            'large_text': 'Monika After Story',
            'large_image': 'maslogo',
        }
    }


    def check_ani():
        if store.mas_anni.isAnni():
            return "Today is our " + store.mas_anni.anniCount() + " year anniversary!"
        if store.mas_anni.isAnniSixMonth():
            return "Today is our 6 month anniversary!"
        if store.mas_anni.isAnniThreeMonth():
            return "Today is our 3 month anniversary!"
        if store.mas_anni.isAnniOneMonth():
            return "Today is our first one month anniversary!"
        if store.mas_anni.isAnniWeek():
            return "Today is our first week anniversary!"
        return None
        
        

    # Runs with ch30_minute updates activity with new data
    def update_activity(client):
        import random

        ping = None
        # Ping RPC server to check connection is still alive
        try:
            ping = client.ping()
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

        # Custom message
        if store.persistent.rpc_use_custom and custom_rpc_file != 'auto':
            new_act['details'] = custom_rpc_file
        
        # Brb check
        # If the last brb_label is the same as the current label
        # then dont pick again otherwise the presence will keep changing every minute and it just looks weird imo
        elif store.persistent.rpc_use_brb_status and store.mas_idle_mailbox.read(3) is not None:
            cur_brb_label = store.mas_idle_mailbox.read(3)
            # Prevnts picking random every minute cuz thats stupid
            if cur_brb_label == store.kventis_rpc.rpc_last_brb_label:
                new_act['details'] = store.kventis_rpc.rpc_last_brb.format(monika=store.m_name)
            else:
                brb_text = store.kventis_rpc_reg.BRB_TEXT_MAP.get(cur_brb_label, None)
                if brb_text is not None:
                    if isinstance(brb_text, list):
                        brb_text = random.choice(brb_text)
                    new_act['details'] = brb_text.format(monika=store.m_name)
                    store.kventis_rpc.rpc_last_brb = brb_text
                    store.kventis_rpc.rpc_last_brb_label = cur_brb_label

        # Location data and aniversary check
        ani = check_ani()
        if ani is None and store.persistent.rpc_use_room_status:
            room_text = store.kventis_rpc_reg.ROOM_TEXT_MAP.get(store.persistent._mas_current_background, None)
            room = store.mas_background.BACKGROUND_MAP.get(store.persistent._mas_current_background, None)
            if room_text is None and room is None:
                new_act['state'] = "In the " + store.persistent._mas_current_background
            elif room_text is None:
                new_act['state'] = "In the " + room.prompt
            else:
                new_act['state'] = "In the spaceroom"
        elif ani is not None:
            new_act['state'] = ani
        

        # Finally set activity
        try:
            client.activity(new_act)
        except Exception as e:
            log('warn', 'Failed to set activity: ' + str(e))

    # get custom file
    def read_custom():
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
            if not os.path.exists(rpc_base):
                try:
                    os.mkdir(rpc_base)
                except:
                    log('warn', 'Cannot make path' + rpc_base + ' all RPC custom will be disabled')
                    return
            with open(custom_rpc_file_path, "w+") as f:
                f.seek(0,2) # Windows
                f.write("auto")
                f.close
        return

    # Toggles client on/off
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
            return
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
            return

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
                        log('error', 'Problem starting socket ' + str(e))
                        return False
                    else:
                        return True
            else:
                log('warn', 'Could not find discord socket unable to start RPC')
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
                    self.s_sock = open(pos_path, "w+b")
                except:
                    # Didnt find path that doesnt suck
                    pass
                else:
                    # Found a path that does suck and works thats cool
                    return True
            else:
                log('error', 'Could not find a vaild path for discord RPC')
                # Cringe tbh
                return False

        def receive(self, size):
            return self.s_sock.read(size)

        def write(self, data):
            # Seriously dont understand windows what is the point in 
            # any of this
            self.s_sock.seek(0,2)
            self.s_sock.write(data)
            self.s_sock.flush()

    def gen_client():
        # Unix 💪
        if renpy.windows:
            log('info', 'Creating windows client')
            return DiscordClientWin()
        else:        
            log('info', 'Creating unix client')
            return DiscordClientUnix() 

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

        # Important otherwise things get messy after a certain ammount of MAS restarts without computer reboot
        store.mas_submod_utils.registerFunction("quit", client.close)

    if store.persistent.rpc_use_custom:
        read_custom()