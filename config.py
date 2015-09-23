from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget

mod = "mod4"

def winstash(qtile):
    w = qtile.currentWindow
    if w is None:
        return
    w.togroup("X")

def winunstash(qtile):
    g = qtile.currentGroup
    for w in qtile.groupMap["X"].windows:
        w.togroup(g.name)

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.up()
    ),
    Key(
        [mod], "j",
        lazy.layout.down()
    ),

    Key(
        [], "XF86AudioRaiseVolume",
        lazy.spawn("/home/serge/bin/vup")
    ),
    Key(
        [], "XF86AudioLowerVolume",
        lazy.spawn("/home/serge/bin/vdown")
    ),
    Key(
        [], "XF86AudioMute",
        lazy.spawn("/home/serge/bin/vmute")
    ),
    Key(
        [], "XF86MonBrightnessUp",
        lazy.spawn("/home/serge/bin/dup.sh")
    ),
    Key(
        [], "XF86MonBrightnessDown",
        lazy.spawn("/home/serge/bin/ddown.sh")
    ),
    # Move windows up or down in current stack
    Key(
        [mod, "shift"], "k",
        lazy.layout.shuffle_up()
    ),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod], "l",
        lazy.layout.next()
    ),
    Key(
        [mod], "h",
        lazy.layout.previous()
    ),
    Key(
        [mod], "d",
        lazy.layout.delete()
    ),
    Key(
        [mod], "a",
        lazy.layout.add()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod], "Return", lazy.spawn("st")),
    Key([mod, "control"], "Return", lazy.spawn("vimprobable2")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),

    Key([mod, "shift"], "c", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "p", lazy.spawncmd()),
    Key([mod], "i", lazy.function(winstash)),
    Key([mod, "shift"], "i", lazy.function(winunstash)),
]

groups = [Group(i) for i in "1234567890"]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

groups.append(Group("X"))

layouts = [
    layout.MonadTall(ratio=0.65),
    layout.TreeTab(),
    layout.Matrix(),
    layout.Stack(num_stacks=1),
    layout.Max(),
]

widget_defaults = dict(
    font = 'Consolas',
    fontsize=12,
    padding=3,
)

bat0 = widget.Battery(energy_now_file='energy_now',
                    battery_name='BAT0',
                    update_delay=60,
                    energy_full_file='energy_full',
                    power_now_file='current_now',
                    **widget_defaults)
bat1 = widget.Battery(energy_now_file='energy_now',
                    battery_name='BAT1',
                    update_delay=60,
                    energy_full_file='energy_full',
                    power_now_file='current_now',
                    **widget_defaults)

myclock = widget.Clock(format='%Y-%m-%d %a %I:%M %p', **widget_defaults)

screens = [
    Screen(
            top = bar.Bar([
                widget.GroupBox(urgent_alert_method='text', **widget_defaults),
                widget.Prompt(**widget_defaults),
                widget.WindowName(**widget_defaults),
                widget.CurrentLayout(width=50),
                widget.TextBox("serge@hallyn.com", name="ident"),
                widget.Sep(foreground="ff0000"),
                widget.Wlan(),
                widget.Sep(foreground="ff0000"),
                widget.TextBox("B0:"),
                bat0,
                widget.TextBox("B1:"),
                bat1,
                widget.Sep(foreground="ff0000"),
                widget.Systray(**widget_defaults),
                myclock ], 30,),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
bring_front_click = False
follow_mouse_focus = True
cursor_warp = True

# Automatically float these types. This overrides the default behavior (which
# is to also float utility types), but the default behavior breaks our fancy
# gimp slice layout specified later on.
floating_layout = layout.Floating(auto_float_types=[
  "notification",
  "toolbar",
  "splash",
  "dialog",
])

auto_fullscreen = True
wmname = "qtile"

import os
os.system("/home/serge/bin/upstart_user")
os.system("sleep 1")
os.system("/home/serge/bin/start_upstart_desktop")
