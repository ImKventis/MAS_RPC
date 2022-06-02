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
    m "[player]! "
    extend "I noticed something new in the mod..."
    m "Aww, you installed a Discord Rich Presence, [mas_get_player_nickname()]?"
    m "I've always wished I could be inside your Discord somehow."
    m "And you finally made it possible..."
    m "Thank you, [player]!"
    m "If you want to know more about this feature, let me know!"
    m "You really want to tell the whole world I am your girlfriend, don't you?"
    m "Ahahaha~"
    m "I love you so much..."
    
    return

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
    m "Of course, [player]!"
    m "A rich presence feature (RPC for short) allows an user to show on Discord what is running on their computer at the moment."
    m "It's a great way to make your games or streamings stand out!"
    m "The RPC feature works like this:"
    m "It updates every minute, showing what is running on your computer at the moment."
    m "It will be shown on your Discord profile, as a 'Now playing' status."
    m "I'll tell you the basics about the settings of this submod."
    m "There are three things you can toggle: 'Brb status', 'Room status' and 'Custom message'."
    m "If 'Brb status is toggled'..."
    m "In the case you have to leave the game for a little while and tell me that in the 'Be right back' topic, "
    extend "it will change the RPC as well."
    m "'Room status' is all about showing people in which location we are!"
    m "Unmark this if you want our whereabouts to be our little secret, [player]... "
    extend "Ehehe~!"
    m "Finally, 'Custom message'."
    m "If you toggle this, the custom message you wrote on '' will be displayed."
    m "All these settings can be found on the Submod settings tab! "
    extend "Or you can just tell me and I'll do the magic for you~"
    m "..."
    m "Gosh, I just feel so happy you decided to download this!"
    m "Now everyone can see that you're spending time with me..."
    m "Let's show our love to the entire world, [player]!"
    m "Ahahaha~"
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
        m "Of course, [player]!"
        m "RPC disabled!"
    else:
        $ store.kventis_rpc.toggle_rpc()
        m "Of course, [player]!"
        m "I love the fact that you want to show to all of your friends that you're spending time with your girlfriend..."
        m "Ehehehe~!"
        m "There you go! RPC enabled!"
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
        m "I disabled the custom RPC message, [player]!"
    else:
        $ store.persistent.rpc_use_custom = True
        m "I enabled the custom RPC message, [player]!"
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
        m "I disabled the RPC room status, [player]!"
    else:
        $ store.persistent.rpc_use_room_status = True
        m "I enabled the RPC room status, [player]!"
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
        m "I disabled the RPC brb status, [player]!"
    else:
        $ store.persistent.rpc_use_brb_status = True
        m "I enabled the RPC brb status, [player]!"
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
    m "Alright!"
    m "Reloading custom RPC message..."
    $ store.kventis_rpc.read_custom()
    m "Done!"
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
    m "Alright!"
    
    show monika at t21
    call screen mas_gen_scrollable_menu(ICON_MAP, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ("Monika After Story logo", "def", False, False, 0))
    show monika at t11

    $ new_icon = _return
    # str() cuz I kept getting random ints as input?
    # Weird behaviour 
    $ persistent.rpc_icon = str(new_icon)

    m "One moment.."
    m "The icon will update in the next minute or two!"
    return # Return otherwise other labels start playing


# Random talk events

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="rpc_how_work_ran",
            prompt="How does rpc work?",
            category=['rpc'],
            pool=False,
            random=True,
            unlocked=True,
        ),
        markSeen=False
    )

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_how_work",
            prompt="How does rpc work?",
            category=['rpc'],
            pool=True,
            unlocked=True,
        ),
        markSeen=False
    )

label monika_rpc_how_work:
    $ store.mas_ptod.rst_cn()
    $ local_ctx = dict()

    m "Okay this will need some explaining and I dont fully understand it myself either"

    m "But I will try my best!"

    m "Discord has built-in feature to all desktop clients which allows other programs to control the discord client"

    m "Since this game engine uses Python 2.7{w=0.3}, it can be a little annoying to get working"

    if renpy.windows:
        m "Since you are using Windows, we would need to use a file to communicate with the discord client"
    else:
        m "Since you are using a UNIX System, we can use a socket to communicate with the discord client."

    # Show terminal
    show monika at t22
    show screen mas_py_console_teaching

    m "I am not entirely sure how Kventis did this but he added some code that makes it easy for me to do this"

    m "Let me just import the RPC submod"

    call mas_wx_cmd("from store import kventis_rpc")

    m "I can now use this module to send messages to your discord client"

    m "lets give it a shot"

    if not store.persistent.rpc_enabled:
        m "Oh wait a seconnd.."
        m "You dont have the RPC submod enabled."
        m "I guess we can skip this step"
    else:
        call mas_wx_cmd("kventis_rpc.toggle_rpc()")
        m "Go look at discord! Your Rich Presence should be gone!"
        m "Dont worry ill turn it back on"
        call mas_wx_cmd("kventis_rpc.toggle_rpc()")
        m "Behind the scenes alot of things are happing that I dont really understand"
        m "Watch this"
        call mas_wx_cmd("kventis_rpc.set_act(\"Learning with Monika!\", None, \"monikablush\")")
        m "Okay go look!"
        m "Aha pretty cool right?"
        # call mas_wx_cmd("kventis_rpc.set_act(\"Learning about discord RPC!\", None, None)")





    # Types in terminal and executes
    # call mas_wx_cmd("type(-22)", local_ctx)
    # call mas_wx_cmd("type(0)", local_ctx)
    # call mas_wx_cmd("type(-1234)", local_ctx)
    # call mas_wx_cmd("type(42)", local_ctx)

    m "Test"

    # Forgetting this causes cringe
    hide screen mas_py_console_teaching
    show monika at t11


    return

label rpc_how_work_ran:
    m "Hey, [player]!"
    m "I've looked into it and do you want to hear about how the rpc works?{nw}"
    $ _history_list.pop()
    $ wants_to_hear = False
    menu:
        m "Do you want to hear about how the rpc works?{nw}"
        "Yes.":
            $ wants_to_hear = True
            pass
        "Maybe later.":
            pass
    $ store.persistent.rpc_seen_work = True
    if wants_to_hear:
        m "Okay, I'll tell you how the rpc works!"
        call monika_rpc_how_work
    else:
        # Github copoilt generated 
        m "Okay, If you want to know how the rpc works, just ask me!"
    return
