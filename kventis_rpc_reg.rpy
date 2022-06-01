
# Large register of..
# Brbs to message
# Backgrounds to messages
#get_idle_cb
#_mas_idle_data.read(3) = get currenet label

#https://github.com/Monika-After-Story/MonikaModDev/blob/24f6643c5e80787d8c40f62ab7d53a1173f56d41/Monika%20After%20Story/game/zz_backgrounds.rpy
#    class MASFilterableBackground(object):
init python in kventis_rpc_reg:
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

    BRB_TEXT_MAP = {
        'monika_brb_idle_callback' : 'AFK',
        'monika_writing_idle_callback' : ['Writing with {monika}', 'Writing {monika} a love poem'],
        'monika_idle_game_callback' : 'Gaming with {monika}',
        'monika_idle_coding_callback' : ['Creating bugs with {monika}', 'Developing with {monika}', 'Coding with {monika}', '127.0.0.1/{monika}', 'def {monika}() -> \'love\''],
        'monika_idle_reading_callback': 'Reading with {monika}',
        'monika_idle_workout_callback' : 'Working out with {monika}',
        'monika_idle_nap_callback' : ['Napping with {monika}', 'Snuggling with {monika}'], 
        'monika_idle_shower_callback': ['Showering', '{monika} is waiting me come out of the shower!'],
        'monika_idle_homework_callback' : ['Doing homework', 'Learning with {monika}', 'Smart time with {monika}'],
        'monika_idle_working_callback' : 'Working on something',
        'monika_idle_screen_break_callback' : ['Taking a break from the screen', 'Touching grass'],
        'monika_writing_idle_callback' : ['Writing with {monika}', 'Writing {monika} a love poem'],
        # u/geneTechnician watching SubMod
        # Suggested by u/lost_localcat
        '_mas_watching_you_draw': "Drawing with {monika}",
        '_mas_watching_you_game': "Gaming with {monika}",
        '_mas_watching_you_code': ['Creating bugs with {monika}', 'Developing with {monika}', 'Coding with {monika}', '127.0.0.1/{monika}', 'def {monika}() -> \'love\''],
        '_watching': ['Watching something with {monika}', 'Netflix and Chill with {monika}']
    }

    # Map of icons to choose from
    # DOES NOT ALLOW CUSTOM JSONS DUE TO IDIOTCORD
    ICON_MAP = [
        # Default mas logo
        ("Dev Icon", "testicon", False, False),
        ("Chibi Monika", "chibi", False, False)
    ]
    
    # List of rooms id to text
    # none by default
    ROOM_TEXT_MAP = {}

    # Loads the map json and merges into BRB_TEXT_MAP
    def load_map_file(m_type,name, map):
        import json
        path = os.path.join(m_type, name)
        store.kventis_rpc.log('info', path)
        if os.path.exists(path):
            with open(path, "r") as f:
                json_str = f.read()
                j_map = None
                try:
                    j_map = json.loads(json_str)
                except:
                    store.kventis_rpc.log('warn', name + ' is not a vaild json file.')
                if j_map is not None:
                    map.update(j_map)
        else:
            store.kventis_rpc.log('warn', 'Could not load map file' + name)

    # Only a function because return cannot be used in init python:
    def load_maps():
        if failed_make_paths:
            store.kventis_rpc.log('warn', "Failed to read one of the rpc_map paths. Custom Maps will be disabled")
            return

        for file in os.listdir(rpc_b_maps):
            load_map_file(rpc_b_maps, file, BRB_TEXT_MAP)

        for file in os.listdir(rpc_r_maps):
            load_map_file(rpc_r_maps, file, ROOM_TEXT_MAP)

    load_maps()


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="rpc_failed_custom_empty"
        )
    )

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="rpc_failed_custom_too_long"
        )
    )



label rpc_failed_custom_empty:
    m "[player]... I'm sorry, I couldn't find the custom_presence.txt file."
    m "because theres nothing in it."
    m "To prevent further problems I have disabled custom rpc message for you."
    return

label rpc_failed_custom_too_long:
    m "[player]... I'm sorry, I couldn't find the custom_presence.txt file."
    m "because it was too long."
    m "To prevent further problems I have disabled custom rpc message for you."
    return