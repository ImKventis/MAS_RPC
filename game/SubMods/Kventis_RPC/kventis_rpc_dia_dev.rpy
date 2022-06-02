
# Dev Dialouge does not need to be pretty but needs to be functional


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_rpc_dev_test_blocking",
            prompt="DEV: Can you test RPC blocking",
            category=['rpc'],
            pool=True,
            unlocked=True,
        ),
        markSeen=False
    )

label monika_rpc_dev_test_blocking:
    m "Alright!"
    m "Blocking for 3 minutes"
    $ store.kventis_rpc.set_act('Testing something with {monika}', None, None)
    $ store.kventis_rpc.block_for(3)
    m "Done!"
    return # Return otherwise other labels start playing