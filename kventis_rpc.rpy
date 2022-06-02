
# Submod made with love by u/KventisAndM and with help from u/my-otter-self
# https://github.com/ImKventis


init -990 python in mas_submod_utils:
    Submod(
        author="Kventis",
        name="Discord RPC",
        description="Allows Monika to access your discord and change your status.\nLet the world know!",
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
    import time
    import store


    def log(msg_type, msg):
        if msg_type == "info":
            store.mas_submod_utils.submod_log.info("[Discord RPC] " + msg)
        elif msg_type == "warn":
            store.mas_submod_utils.submod_log.warning("[Discord RPC] " + msg)
        else:
            store.mas_submod_utils.submod_log.error("[Discord RPC] " + msg)

    # Client stuff
    client_id = '977282947981910026'
    client = None
    # Folder stuff
    rpc_base = os.path.join(renpy.config.basedir, "./rpc/")
    custom_rpc_file_path = os.path.join(rpc_base, "custom_presense.txt")
    custom_rpc_file = None
    block_value = 0
    cur_act = {}
    # Brb stuff
    last_brb = None
    last_brb_label = ''


    # Honestly not sure if this is even needed but I'm keeping it for now
    if store.persistent.rpc_enabled is None:
        store.persistent.rpc_enabled = True
    
    if store.persistent.rpc_use_custom is None:
        store.persistent.rpc_use_custom = False

    if store.persistent.rpc_use_brb_status is None:
        store.persistent.rpc_use_brb_status = True

    if store.persistent.rpc_use_room_status is None:
        store.persistent.rpc_use_room_status = True

    if store.persistent.rpc_icon is None:
        store.persistent.rpc_icon = 'def'


    start_time = int(time.time())
    default_act = {
        'timestamps': {
            'start': start_time
        },
        'assets': {
            'large_text': 'Monika After Story',
            'large_image': 'def',
        }
    }
    # loads when ch30-minute hasnt been updated yet
    loading_act = {
        'details': 'Waiting for RPC...',
        'state': 'waiting for next update',
        'timestamps': {
            'start': start_time
        },
        'assets': {
            'large_text': 'Monika After Story',
            'large_image': 'def',
            'small_image': 'loading_cirlce',
            'small_text': 'Loading..'
        }
    }

    def get_from_map(_key, _map):
        from random import choice
        _text = _map.get(_key, None)
        if _text is None:
            return None
        if isinstance(_text, list):
            return choice(_text)
        return _text

    def check_ani():
        from store import mas_anni
        if mas_anni.isAnni():
            return "Today is our " + mas_anni.anniCount() + " year anniversary!"
        if mas_anni.isAnniSixMonth():
            return "Today is our 6 month anniversary!"
        if mas_anni.isAnniThreeMonth():
            return "Today is our 3 month anniversary!"
        if mas_anni.isAnniOneMonth():
            return "Today is our first one month anniversary!"
        if mas_anni.isAnniWeek():
            return "Today is our first week anniversary!"
        return None

    def check_brb():
        global last_brb_label
        global last_brb
        from store import kventis_rpc_reg, persistent, mas_idle_mailbox
        from store.kventis_rpc_reg import BRB_TEXT_MAP

        cur_brb_label = mas_idle_mailbox.read(3)
        details = None

        # u/geneTechnician watching SubMod
        # Suggested by u/lost_localcat
        if cur_brb_label == "watching_something_callback":
            if persistent._mas_watching_you_code:
                details = get_from_map('_mas_watching_you_code', BRB_TEXT_MAP)
            elif persistent._mas_watching_you_draw:
                details = get_from_map('_mas_watching_you_draw', BRB_TEXT_MAP)
            elif persistent._mas_watching_you_game:
                details = get_from_map('_mas_watching_you_game', BRB_TEXT_MAP)
            else:
                details = get_from_map('_watching', BRB_TEXT_MAP)

        elif cur_brb_label == last_brb_label:
            details = last_brb
    
        else:
            brb_text = get_from_map(cur_brb_label, BRB_TEXT_MAP)
            if brb_text is not None:
                details = brb_text
            else:
                details = "Afk"

        last_brb = details
        last_brb_label = cur_brb_label
        return details      

    def check_room():
        from store import persistent, kventis_rpc_reg, mas_background
        from store.kventis_rpc_reg import ROOM_TEXT_MAP
        room_text = ROOM_TEXT_MAP.get(store.persistent._mas_current_background.lower())
        room = mas_background.BACKGROUND_MAP.get(store.persistent._mas_current_background, None)
        state = None
        if room_text is not None:
            state = room_text
        elif room is not None:
            state = "In the " + room.prompt
        else:
            state = "In the spaceroom"
        return state

    def check_details():
        # Brb check
        from store import mas_idle_mailbox, persistent
        details = None
        if persistent.rpc_use_brb_status and mas_idle_mailbox.read(3) is not None:

            details = check_brb()

        # Custom message after brb as overwrite
        elif persistent.rpc_use_custom and custom_rpc_file != 'auto':

            details = custom_rpc_file

        return details

    def check_state():
        from store import persistent
        ani = check_ani()
        state = None
        if ani is None and persistent.rpc_use_room_status:
            state = check_room()
        elif ani is not None:
            state = ani
        return state

    # Heh heh
    # ASSets
    # Heh heh
    def load_ass():
        from store import persistent
        d = {
            'large_text': 'Monika After Story',
            'large_image': 'def',
        }
        if persistent.rpc_icon != 'def':
            d['large_image'] = persistent.rpc_icon
            d['small_image']= 'def'
            d['small_text'] = 'MAS'
        return d

    
    def set_act(details, room, icon):
        from store import m_name
        global cur_act
        act = {'timestamps': {'start': start_time}}

        # print "Starting set act"

        if details is None:
            details = check_details()
            if details is None:
                act['details'] = "Spending time with " + m_name
            else:
                act['details'] = details.format(monika=m_name)
        else:
            act['details'] = details.format(monika=m_name)

        if room is None:
            state = check_state()
            if state is not None:
                act['state'] = state
        else:
            act['state'] = room

        if icon is None:
            act['assets'] = load_ass()
        else:
            act['assets'] = icon

        # In case we need it for later
        cur_act = act


        try:
            client.activity(act)
        except Exception as e:
            log('warn', 'Failed to set activity: ' + str(e))

    def block_for(minutes):
        global block_value
        block_value += minutes

    # Runs with ch30_minute updates activity with new data
    def update_activity(client):
        global block_value

        ping = None
        # Ping RPC server to check connection is still alive
        try:
            ping = client.ping()
        except:
            pass
        
        # Connection is dead rip
        if ping is None:
            try:
                client.start()
            except:
                # It aint happening retry on next minute cuz cringe 
                return

        # Should block
        # Pain note: Couldnt fiqure out how why update_activity wouldnt start turns out 
        # The ">" was the wrong way round
        if block_value > 0:
            block_value -= 1
            return

        set_act(None, None, None)
        
    # get custom file
    # Pain
    def read_custom():
        global custom_rpc_file
        if os.path.exists(custom_rpc_file_path):
            f = open(custom_rpc_file_path, "r")
            try:
                custom_rpc_file = f.read()
                f.close()
            except Exception as e:
                log('warn', 'Failed to read custom file: ' + str(e))
                custom_rpc_file = 'auto'
            if len(custom_rpc_file) == 0:
                store.persistent.rpc_use_custom = False
                log("warn", "Custom RPC file is empty, disabling custom RPC")
                store.queueEvent("rpc_failed_custom_empty")
            elif len(custom_rpc_file) > 200:
                store.persistent.rpc_use_custom = False
                store.queueEvent("rpc_failed_custom_too_long")
                log("warn", "Custom RPC file is too long, disabling custom RPC")
        else:
            log("info", "Custom RPC file not found, creating default")
            if not os.path.exists(rpc_base):
                try:
                    os.mkdir(rpc_base)
                except:
                    log('warn', 'Cannot make path' + rpc_base + ' all RPC custom will be disabled')
                    return 
            try:
                f = open(custom_rpc_file_path, "w+")
                f.seek(0,2) # Windows ( >︹<)
                f.write("auto")
                f.close
            except Exception as e:
                log('warn', 'Failed to create default custom file: ' + str(e))
        return

    # Toggles client on/off
    def toggle_rpc():
        from store import persistent, mas_submod_utils

        if persistent.rpc_enabled:
            persistent.rpc_enabled = False

            try:
                client.close()
            except Exception as e:
                log('warn', 'Failed to close.: ' + str(e))

            log('info', 'RPC Disabled')

            mas_submod_utils.unregisterFunction(
                "ch30_minute",
                update_activity
            )

            mas_submod_utils.unregisterFunction("quit", client.close)
            return
        else:
            persistent.rpc_enabled = True
            try:
                client.start()
            except Exception as e:
                log('error', "Failed to start client " + str(e))
            log('info', 'RPC Enabled')

            if client.connected:
                update_activity(client)

            mas_submod_utils.registerFunction(
                "ch30_minute",
                update_activity,
                args=[client]
            )

            # Important on windows (cringe) kept causing issues
            mas_submod_utils.registerFunction("quit", client.close)
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
            except Exception as e:
                log('warn', 'Failed to close: ' + str(e))
                pass
            status = self.connect()
            if self.connected:
                try:
                    self.handshake()
                except Exception as e:
                    log('warn', 'Failed to handshake: ' + str(e))
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
            self.s_sock = socket.socket(socket.AF_UNIX)
            # Wouldnt boot forever otherwise
            self.s_sock.settimeout(3)
            for i in range(10):
                path = pos_path.format(i)
                if os.path.exists(path):
                    try:
                        self.s_sock.connect(path)
                    except OSError as e:
                        pass
                    except:
                        log('error', 'Problem starting socket ' + str(e))
                        return False
                    else:
                        return True
            else:
                log('warn', 'Could not find discord socket unable to start RPC. Possible discord is not running.')
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
                except Exception as e:
                    log("warn", "Handshake failed: " + str(e))
                    self.connected = False

        def connect(self):
            from io import open
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
            self.s_sock.write(data)
            self.s_sock.flush()

    def gen_client():
        # Unix pog 💪
        # - Someone prlly
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