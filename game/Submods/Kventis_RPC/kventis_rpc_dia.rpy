# Dialogue


# Thanks to u/my-otter-self on Reddit for Monika's dialogue!


# Runs once when first installed
# Monika talks about wishing she could access discord so maybe?
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="kventis_rpc_installed",
            conditional="True",
            action=EV_ACT_QUEUE,
        )
    )

# Needs doing
label kventis_rpc_installed:
    m 1suo "[player]! "
    extend 1suu "I noticed something new in the mod..."
    m 1hubla "Aww, you installed a Discord Rich Presence, [mas_get_player_nickname()]?"
    m 1hubsb "I've always wished I could be inside your Discord somehow."
    m 5fubfa "And you finally made it possible..."
    m 5hubfa "Thank you, [player]!"
    m 3wubfb "If you want to know more about this feature, let me know!"
    m 3tubfu "You really want to tell the whole world I am your girlfriend, don't you?"
    m 1hubfb "Ahahaha~"
    m 1fubfa "I love you so much..."
    return "love"

# Explains RPC and the features
# RPC Updates every minute
# Brb status = Changes the status based on which beb has been selected
# Custom message = Uses the message from rpc/custom_presence.txt above all else
# Room status = Changes the status based on the room the user is in
# Mention how you can ask monika to reload custom_message and toggle features 
# or change features from the submod settings menu
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_explain",
            prompt="Can you explain RPC?",
            category=['rpc'],
            pool=True,
            unlocked=True,
        ),
        markSeen=False
    )

label monika_rpc_explain:
    m 7hua "Of course, [player]!"
    m 7rud "A rich presence feature (RPC for short) allows an user to show on Discord what is running on their computer at the moment."
    m 4sub "It's a great way to make your games or streamings stand out!"
    m 1dud "The RPC feature works like this:"
    m 3eud "It updates every minute, showing what is running on your computer at the moment."
    m 3lud "It will be shown on your Discord profile, as a 'Now playing' status."
    m 3wua "I'll tell you the basics about the settings of this submod."
    m 1dub "There are three things you can toggle: 'Brb status', 'Room status' and 'Custom message'."
    m 1rud "If 'Brb status is toggled'..."
    m 1wud "In the case you have to leave the game for a little while and tell me that in the 'Be right back' topic, "
    extend 1wuu "it will change the RPC as well."
    m 7wub "'Room status' is all about showing people in which location we are!"
    m 7tub "Unmark this if you want our whereabouts to be our little secret, [player]... "
    extend 2hub "Ehehe~!"
    m 2wub "Finally, 'Custom message'."
    m 2dud "If you toggle this, the custom message you wrote on '' will be displayed."
    m 4sub "All these settings can be found on the Submod settings tab! "
    extend 4kua "Or you can just tell me and I'll do the magic for you~"
    m 1dubsu "..."
    m 5hubfb "Gosh, I just feel so happy you decided to download this!"
    m 5fubfa "Now everyone can see that you're spending time with me..."
    m 3kubfa "Let's show our love to the entire world, [player]!"
    m 1hubfb "Ahahaha~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_toggle",
            prompt="Can you toggle the RPC?",
            category=['rpc'],
            pool=True,
            unlocked=True,
        ),
        markSeen=False
    )

# Toggle RPC
label monika_rpc_toggle:
    if store.persistent.rpc_enabled:
        $ store.kventis_rpc.toggle_rpc()
        m 1hub "Of course, [player]!"
        m "RPC disabled!"
    else:
        $ store.kventis_rpc.toggle_rpc()
        m 1hub "Of course, [player]!"
        m 5tubsu "I love the fact that you want to show to all of your friends that you're spending time with your girlfriend..."
        m 5hubfa "Ehehehe~!"
        m 4hubfa "There you go! RPC enabled!"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_toggle_custom",
            prompt="Can you toggle the custom RPC message?",
            category=['rpc'],
            pool=True,
            unlocked=True,
        ),
        markSeen=False
    )

label monika_rpc_toggle_custom:
    if store.persistent.rpc_use_custom:
        $ store.persistent.rpc_use_custom = False
        m 1hub "I disabled the custom RPC message, [player]!"
    else:
        $ store.persistent.rpc_use_custom = True
        m 1hub "I enabled the custom RPC message, [player]!"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_toggle_room",
            prompt="Can you toggle the RPC room status?",
            category=['rpc'],
            pool=True,
            unlocked=True,
        ),
        markSeen=False
    )

label monika_rpc_toggle_room:
    if store.persistent.rpc_use_room_status:
        $ store.persistent.rpc_use_room_status = False
        m 1hub "I disabled the RPC room status, [player]!"
    else:
        $ store.persistent.rpc_use_room_status = True
        m 1hub "I enabled the RPC room status, [player]!"
    return
    
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_toggle_brb",
            prompt="Can you toggle the RPC brb status?",
            category=['rpc'],
            pool=True,
            unlocked=True,
        ),
        markSeen=False
    )

label monika_rpc_toggle_brb:
    if store.persistent.rpc_use_brb_status:
        $ store.persistent.rpc_use_brb_status = False
        m 1hub "I disabled the RPC brb status, [player]!"
    else:
        $ store.persistent.rpc_use_brb_status = True
        m 1hub "I enabled the RPC brb status, [player]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_reload_custom",
            prompt="Can you reload the RPC custom message?",
            category=['rpc'],
            pool=True,
            unlocked=True,
        ),
        markSeen=False
    )

label monika_rpc_reload_custom:
    m 1hub "Alright!"
    m 1dud "Reloading custom RPC message..."
    $ store.kventis_rpc.read_custom()
    m 1hub "Done!"
    return # Return otherwise other labels start playing

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_change_icon",
            prompt="Can you change the RPC icon?",
            category=['rpc'],
            pool=True,
            unlocked=True,
        ),
        markSeen=False
    )

# Place holder for RPC icon change
label monika_rpc_change_icon:
    $ from store import persistent
    $ from store.kventis_rpc_reg import ICON_MAP
    m 1hub "Alright!"
    
    show monika at t21
    call screen mas_gen_scrollable_menu(ICON_MAP, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ("Monika After Story logo", "def", False, False, 0))
    show monika at t11

    $ new_icon = _return
    # str() cuz I kept getting random ints as input?
    # Weird behaviour 
    $ persistent.rpc_icon = str(new_icon)

    m 1dud "One moment..."
    m 1hub "The icon will update in the next minute or two!"
    return # Return otherwise other labels start playing
