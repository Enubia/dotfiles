# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import socket
import subprocess

from libqtile import layout, bar, widget, hook
from libqtile.command import lazy
from libqtile.config import Key, Screen, Group, Drag

import arcobattery

# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


keys = [
    # SUPER + FUNCTION KEYS
    Key([mod], "c", lazy.spawn('conky-toggle')),
    Key([mod], "w", lazy.spawn('firefox')),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "r", lazy.spawn('rofi-theme-selector')),
    Key([mod], "x", lazy.spawn('arcolinux-logout')),
    Key([mod], "space", lazy.spawn('rofi -show run')),
    Key([mod], "Escape", lazy.spawn('xkill')),
    Key([mod], "Return", lazy.spawn('termite')),

    # SUPER + SHIFT KEYS
    Key([mod, "shift"], "Return", lazy.spawn('thunar')),
    Key([mod, "shift"], "space", lazy.spawn('rofi -show drun')),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "control"], "r", lazy.restart()),

    # VARIETY KEYS
    Key(["mod1", "shift"], "4", lazy.spawn('xfce4-screenshooter')),

    # INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),

    # INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

    #    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    #    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
    #    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
    #    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),

    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.next_layout()),

    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),

    # RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),

    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
    Key([mod, "shift"], "f", lazy.window.toggle_floating()), ]

groups = []

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ]

group_labels = ["", "", "", "", "", "", "", "", "", "", ]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",
                 "monadtall", "monadtall", ]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([
        # CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
        Key([mod, "shift"], i.name, lazy.window.togroup(
            i.name), lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin": 5,
            "border_width": 2,
            "border_focus": "#5e81ac",
            "border_normal": "#4c566a"
            }


layout_theme = init_layout_theme()

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Floating(**layout_theme),
]


# COLORS FOR THE BAR

def init_colors():
    return [["#2F343F", "#2F343F"],  # color 0
            ["#2F343F", "#2F343F"],  # color 1
            ["#c0c5ce", "#c0c5ce"],  # color 2
            ["#fba922", "#fba922"],  # color 3
            ["#3384d0", "#3384d0"],  # color 4
            ["#f3f4f5", "#f3f4f5"],  # color 5
            ["#cd1f3f", "#cd1f3f"],  # color 6
            ["#62FF00", "#62FF00"],  # color 7
            ["#6790eb", "#6790eb"],  # color 8
            ["#a9a9a9", "#a9a9a9"]]  # color 9


colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(
        font="Noto Sans",
        fontsize=12,
        padding=2,
        background=colors[1]
    )


widget_defaults = init_widgets_defaults()


def open_thunar(qtile):
    qtile.cmd_spawn('thunar')


def open_htop(qtile):
    qtile.cmd_spawn('termite -e htop')


def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list_setup = [
        widget.Image(
            filename=home + "/.config/qtile/icons/py.png",
            margin=5,
            mouse_callbacks={'Button1': open_thunar}
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2]
        ),
        widget.GroupBox(
            font="FontAwesome",
            fontsize=16,
            margin_y=2,
            margin_x=0,
            padding_y=6,
            padding_x=5,
            borderwidth=0,
            disable_drag=True,
            active=colors[3],
            inactive=colors[5],
            rounded=False,
            highlight_method="text",
            this_current_screen_border=colors[8],
            foreground=colors[2]
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2]
        ),
        widget.CurrentLayout(
            font="Noto Sans Bold",
            foreground=colors[5]
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2]
        ),
        widget.WindowName(
            font="Noto Sans",
            fontsize=12,
            foreground=colors[5],
        ),
        widget.Image(
            filename=home + "/.config/qtile/icons/download.png",
            margin=3,
        ),
        widget.NetGraph(
            font="Noto Sans",
            fontsize=12,
            bandwidth="down",
            interface="auto",
            fill_color=colors[3],
            foreground=colors[2],
            background=colors[1],
            graph_color=colors[3],
            border_color=colors[2],
            padding=0,
            border_width=1,
            line_width=1,
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2]
        ),
        widget.Image(
            filename=home + "/.config/qtile/icons/cpu.png",
            margin=2,
        ),
        widget.ThermalSensor(
            tag_sensor="Package id 0",
            update_interval=5.0,
            foreground=colors[5],
            foreground_alert=colors[6],
            metric=True,
            padding=3,
            threshold=80
        ),
        widget.CPUGraph(
            border_color=colors[2],
            fill_color=colors[8],
            graph_color=colors[8],
            border_width=1,
            line_width=1,
            core="all",
            type="box",
            mouse_callbacks={'Button1': open_htop}
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2]
        ),
        widget.Image(
            filename=home + "/.config/qtile/icons/ram.png",
            margin=0,
        ),
        widget.Memory(
            font="Noto Sans",
            format='{MemUsed}M/{MemTotal}M',
            update_interval=1,
            fontsize=12,
            foreground=colors[5],
            mouse_callbacks={'Button1': open_htop}
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2]
        ),
        widget.Image(
            filename=home + "/.config/qtile/icons/calendar.png",
            margin=3,
        ),
        widget.Clock(
            foreground=colors[5],
            fontsize=12,
            format="%d-%m-%Y %H:%M"
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2]
        ),
        arcobattery.BatteryIcon(
            padding=0,
            scale=0.7,
            y_poss=2,
            theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
            update_interval=5,
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2]
        ),
        widget.Systray(
            icon_size=20,
            padding=4
        ),
    ]
    return widgets_list_setup


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1_init = init_widgets_list()
    return widgets_screen1_init


def init_widgets_screen2():
    widgets_screen2_init = init_widgets_list()
    return widgets_screen2_init


widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [
        Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26)),
        Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26))
    ]


screens = init_screens()

# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

main = None


@hook.subscribe.startup_once
def start_once():
    home_dir = os.path.expanduser('~')
    subprocess.call([home_dir + '/.config/qtile/scripts/autostart.sh'])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'Arcolinux-welcome-app.py'},
    {'wmclass': 'Arcolinux-tweak-tool.py'},
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'},
    {'wmclass': 'Arandr'},
    {'wmclass': 'feh'},
    {'wmclass': 'Galculator'},
    {'wmclass': 'arcolinux-logout'},
    {'wmclass': 'xfce4-terminal'},
    {'wname': 'branchdialog'},
    {'wname': 'Open File'},
    {'wname': 'pinentry'},
    {'wmclass': 'ssh-askpass'},
    {'wmclass': 'JetBrains Toolbox'},

], fullscreen_border_width=0, border_width=0)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart

wmname = "LG3D"
