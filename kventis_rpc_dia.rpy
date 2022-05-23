# Dialogue


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

# Needs doing
label kventis_rpc_installed:
    m "Placeholder"
    return

# Explains RPC and the features
# Updates every minute
# Brb status = Changes the status based on which beb has been selected
# Custom message = Uses the message from rpc/custom_presence.txt above all else
# Room status = Changes the status based on the room the user is in
# Mention how you can ask monika to reload custom_message
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
    m "Placeholder"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_toggle",
            prompt="Can you turn on the RPC?",
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

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_toggle_custom",
            prompt="Can you toggle a custom RPC message?",
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
        m "I disabled the custom RPC message, [player]!"
