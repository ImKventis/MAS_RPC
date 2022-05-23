
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

    if not os.path.exists(rpc_maps):
        #cringe
        try:
            os.mkdir(rpc_maps)
        except:
            failed_make_paths = True
        
    if not os.path.exists(rpc_b_maps):
        try:
            os.mkdir(rpc_b_maps)
        except:
            failed_make_paths = True
    
    if not os.path.exists(rpc_r_maps):
        try:
            os.mkdir(rpc_r_maps)
        except:
            failed_make_paths = True
    

    BRB_TEXT_MAP = {
        'monika_brb_idle_callback' : 'AFK',
        'monika_writing_idle_callback' : 'Reading with {monika}',
        'monika_idle_game_callback' : 'Gaming with {monika}',
        'monika_idle_coding_callback' : 'Coding away with {monika}',
        'monika_idle_workout_callback' : 'Working out with {monika}',
        'monika_idle_nap_callback' : 'Napping',
        'monika_idle_homework_callback' : 'Doing homework',
        'monika_idle_working_callback' : 'Working on something',
        'monika_idle_screen_break_callback' : ['Taking a break from the screen', 'Touching grass'],
        'monika_writing_idle_callback' : 'Writing something',
    }
    
    # List of rooms id to text
    # none by default
    ROOM_TEXT_MAP = {}

    # Loads the map json and merges into BRB_TEXT_MAP
    def load_map_file(m_type,name):
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
                    BRB_TEXT_MAP.update(j_map)
        else:
            store.kventis_rpc.log('warn', 'Could not load map file' + name)

    # Only a function because return cannot be used in init python:
    def load_maps():
        if failed_make_paths:
            store.kventis_rpc.log('warn', "Failed to read one of the rpc_map paths. Custom Maps will be disabled")
            return

        for file in os.listdir(rpc_b_maps):
            load_map_file(rpc_b_maps, file)

    load_maps()



