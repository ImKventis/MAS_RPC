
# Large register of..
# Brbs to message
# Backgrounds to messages
#get_idle_cb
#_mas_idle_data.read(3) = get currenet label

#https://github.com/Monika-After-Story/MonikaModDev/blob/24f6643c5e80787d8c40f62ab7d53a1173f56d41/Monika%20After%20Story/game/zz_backgrounds.rpy
#    class MASFilterableBackground(object):
init -1 python in kventis_rpc_reg:
    import os
    import store
    
    # Have to manually add Brbs its kinda cringe
    # Op have a custom json which can add other labels to this map
    # Folder of jsons to make submodding easier
    # probs rpc/maps/b/
    rpc_maps = os.path.join(renpy.config.basedir, "./rpc/maps/")
    rpc_b_maps = os.path.join(rpc_maps, "./b/")
    rpc_r_maps = os.path.join(rpc_maps, "./r/")
    failed_make_paths = False

    def log(msg_type, msg):
        if msg_type == "info":
            store.mas_submod_utils.submod_log.info("[Discord RPC] " + msg)
        elif msg_type == "warn":
            store.mas_submod_utils.submod_log.warning("[Discord RPC] " + msg)
        else:
            store.mas_submod_utils.submod_log.error("[Discord RPC] " + msg)

    def checkpath(path):
        global failed_make_paths
        import os
        failed_make_paths = False

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                store.mas_submod_utils.submod_log.info('warn', 'Failed to make path: ' + path)
                failed_make_paths = True
    
    checkpath(rpc_maps)
    checkpath(rpc_b_maps)
    checkpath(rpc_r_maps)

    # Thanks to otter-self again for expanding these.
    BRB_TEXT_MAP = {
        'monika_brb_idle_callback' : 'AFK',
        'monika_writing_idle_callback' : ['Writing with {monika}', 'Writing {monika} a love poem'],
        'monika_idle_game_callback' : ['Gaming with {monika}', '{monika} is my player 2!'],
        'monika_idle_coding_callback' : ['Creating bugs with {monika}', 'Developing with {monika}', 'Coding with {monika}', '127.0.0.1/{monika}', 'def {monika}() -> \'love\''],
        'monika_idle_reading_callback': ['Reading with {monika}', 'Reading {monika} a story'],
        'monika_idle_workout_callback' : ['Working out with {monika}', 'Exercising with {monika}'],
        'monika_idle_nap_callback' : ['Napping with {monika}', 'Snuggling with {monika}'], 
        'monika_idle_shower_callback': ['Showering', '{monika} is waiting me come out of the shower!'],
        'monika_idle_homework_callback' : ['Doing homework', 'Learning with {monika}', 'Smart time with {monika}'],
        'monika_idle_working_callback' : ['Working on something', 'My wife {monika} is waiting me come home from work!'],
        'monika_idle_screen_break_callback' : ['Taking a break from the screen', 'Touching grass'],
        'monika_writing_idle_callback' : ['Writing with {monika}', 'Writing {monika} a love poem'],
        # u/geneTechnician watching SubMod
        # Suggested by u/lost_localcat
        '_mas_watching_you_draw': ['Drawing with {monika}', '{monika} is watching me draw!'],
        '_mas_watching_you_game': ['Gaming with {monika}', '{monika} is my player 2!'],
        '_mas_watching_you_code': ['Creating bugs with {monika}', 'Developing with {monika}', 'Coding with {monika}', '127.0.0.1/{monika}', 'def {monika}() -> \'love\''],
        '_watching': ['Watching something with {monika}', 'Netflix and Chill with {monika}'],
        # u/my-otter-self 's brb submods
        'otter_brb_calling_callback' : ['Someone called me', 'AFK'],
        'otter_brb_food_callback' : ['Grabbing a snack to eat with {monika}', '{monika} is waiting me come back from my snack'],
        'otter_brb_journal_callback' : ['Sharing my journal with {monika}', 'Sharing my daily thoughts with {monika}'],
        'otter_brb_liedown_callback' : ['Napping with {monika}', 'Snuggling with {monika}'], 
        'otter_brb_nails_callback' : ['Doing my nails with {monika}', '{monika} is watching me paint my nails'],
        'otter_brb_plants_callback' : ['Watering my plants', 'Taking care of my plant friends'],
        'otter_brb_socials_callback' : ['Doomscrolling', 'Checking my socials with {monika}'],
        'otter_brb_stim_callback' : ['Stimming with {monika}', '{monika} is waiting while I stim'],
        'otter_brb_stretch_callback' : ['Stretching my legs', 'Touching grass'],
        'otter_brb_vc_callback' : ['On a date with {monika} and my friends', 'Voice chatting with friends'],
        #confiscatedharddrive additions uwu
        'chd_otter_brb_overstimulated_callback' : ['Break due to overstimulation', 'De-stressing with {monika}'],
        'chd_otter_brb_panic_callback' : ['Going through a panic attack', 'Calming down with {monika}'],
        '_mas_listening_to_music' : ['Jamming out with {monika}', 'Vibing with {monika}', 'Listening to music with {monika}'],
        '_mas_listening_to_podcast' : ['From MPR news, I am {monika}', 'Listening to podcast with {monika}', 'Getting informed with {monika}'],
        '_mas_listening_to_drama' : ['Listening to audio drama with {monika}', 'Exploring stories with {monika}'],
        '_listening' : ['Sharing earbuds with {monika}', 'Listening to something with {monika}']
    }

    # Map of icons to choose from
    # DOES NOT ALLOW CUSTOM JSONS DUE TO IDIOTCORD
    # (name, discordassname, False, False)
    ICON_MAP = [
        ("Ribbon", "ribbon", False, False),
        ("My Chibi", "chibi", False, False),
        ("Me Blushing", "monikablush", False, False),
        ("Spaceroom", "spaceroom", False, False),
    ]
    
    # List of rooms id to text
    # none by default due to all rooms being custom
    ROOM_TEXT_MAP = {}

    # Loads the map json and merges into selected map
    def load_map_file(m_type,name, map):
        from json import loads
        path = os.path.join(m_type, name)
        log('info', path)
        if os.path.exists(path):
            with open(path, "r") as f:
                json_str = f.read()
                j_map = None
                try:
                    j_map = loads(json_str)
                except:
                    log('warn', name + ' is not a vaild json file.')
                if j_map is not None:
                    map.update(j_map)
                f.close()
        else:
            log('warn', 'Could not load map file' + name)

    # Only a function because return cannot be used in init python:
    def load_maps():
        if failed_make_paths:
            log('warn', "Failed to read one of the rpc_map paths. Custom Maps will be disabled")
            return

        for file in os.listdir(rpc_b_maps):
            load_map_file(rpc_b_maps, file, BRB_TEXT_MAP)

        for file in os.listdir(rpc_r_maps):
            load_map_file(rpc_r_maps, file, ROOM_TEXT_MAP)

    load_maps()
