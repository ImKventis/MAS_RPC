screen kventis_rpc_setting_pane():
    $ submods_screen_tt = store.renpy.get_screen("submods", "screens").scope["tooltip"]
    vbox:
        box_wrap False
        xfill True
        xmaximum 1000

        hbox:
                style_prefix "check"
                box_wrap False
                textbutton _("Enabled"):
                    action Function(store.kventis_rpc.toggle_rpc)
                    selected persistent.rpc_enabled
                    hovered SetField(submods_screen_tt, "value", ("Enableds Discord Rich Presence integration. "))
                    unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)

                textbutton _("Use custom message"):
                    action ToggleField(persistent, "rpc_use_custom")
                    selected persistent.rpc_use_custom
                    hovered SetField(submods_screen_tt, "value", ("Uses custom_presense.txt instead of generating one."))
                    unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)

                textbutton _("Brb status"):
                    action ToggleField(persistent, 'rpc_use_brb_status')
                    selected persistent.rpc_use_brb_status
                    hovered SetField(submods_screen_tt, "value", ("Use the built in brb statuses"))
                    unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)

                textbutton _("Room status"):
                    action ToggleField(persistent, 'rpc_use_room_status')
                    selected persistent.rpc_use_room_status
                    hovered SetField(submods_screen_tt, "value", ("Mentions what room you are in on the RP"))
                    unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)