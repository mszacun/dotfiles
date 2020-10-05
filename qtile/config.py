# -*- coding: utf-8 -*-
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

import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile import hook
from libqtile.widget.pomodoro import Pomodoro

from widgets.wig30 import Wig30Widget
#from widgets.jakdojade import JakDojadeWidget
from widgets.weather import InteriaWeatherWidget
from widgets.timew import Timew


ALT = 'mod1'
WIN = 'mod4'
TAB = 'Tab'
CTRL = 'control'
SHIFT = 'shift'
RETURN = 'Return'
SPACE = 'space'
mod = WIN

TERMINAL_EMULATOR = 'kitty'

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),
    Key([ALT], "Tab", lazy.layout.down()),

    # Move windows up or down in current stack
    Key(
        [mod, ALT], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, ALT], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),
    Key(
        [mod, CTRL], "space",
        lazy.layout.client_to_next()
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
    Key([mod], "Return", lazy.spawn(TERMINAL_EMULATOR)),
    Key([WIN], "l", lazy.spawn('xlock')),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([CTRL, mod], "j", lazy.next_screen()),
    Key([CTRL, mod], "k", lazy.prev_screen()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    Key([ALT, CTRL], 's', lazy.spawn('spotify')),
    Key([ALT, CTRL], 'f', lazy.spawn('firefox')),
    Key([ALT, CTRL], 'c', lazy.spawn('chromium')),
    Key([ALT, CTRL], 'z', lazy.spawn('zulip')),
    Key([ALT, CTRL], 'p', lazy.spawn('postman')),
    Key([ALT, CTRL], 't', lazy.spawn('thunderbird')),
    Key([ALT, CTRL], 'n', lazy.spawn('nm-applet')),
]

groups = [
    Group('a', spawn=['firefox']),
    Group('s', spawn=[TERMINAL_EMULATOR]),
    Group('d', spawn=['thunderbird']),
    Group('f', spawn=['zulip']),
    Group('g'),
    Group('h'),
    Group('j'),
    Group('k'),
]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

layouts = [
    layout.Max(),
    layout.Tile(ratio=0.5),
]

widget_defaults = dict(
    font='Iosevka',
    fontsize=13,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.TaskList(),
                widget.Systray(),
                widget.TextBox(u' '),
                Timew(),
                widget.TextBox(u' '),
                Pomodoro(num_pomodori=8, length_pomodori=15, length_short_break=2.5),
                widget.TextBox(u' '),
                widget.Clock(format='%Y-%m-%d %a %H:%M'),
            ],
            30,
            background='#181818',
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.TaskList(),
                widget.Systray(),
                #JakDojadeWidget(destination='Reja', start='Plac Strzegomski'),
                widget.TextBox(u' '),
                InteriaWeatherWidget(),
                widget.TextBox(u' '),
                widget.TextBox(u''),
                widget.Volume(foreground='#18BAEB'),
                widget.TextBox(u' '),
                Wig30Widget('ETFDAX'),
                widget.TextBox(u' '),
                Wig30Widget('ETFSP500'),
                widget.TextBox(u' '),
                Wig30Widget('WIG20'),
                widget.TextBox(u' '),
                Wig30Widget('WIGDIV'),
                widget.TextBox(u' '),
                widget.Clock(format='%Y-%m-%d %a %H:%M'),
            ],
            30,
            background='#181818',
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.TaskList(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            30,
            background='#181818',
        ),
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
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"
extentions = []

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen('xbindkeys')
    subprocess.Popen('dunst')
    subprocess.Popen('sh /home/szacun/.screenlayout/2monitors.sh'.split())
    subprocess.Popen('feh --bg-scale /home/szacun/wallpaper.jpg '.split())

@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()
