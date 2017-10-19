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

import re
import subprocess
from datetime import datetime

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile import hook

from libqtile.widget.generic_poll_text import GenPollUrl
from libqtile.widget import base

from bs4 import BeautifulSoup


class Wig30Widget(GenPollUrl):
    url = 'http://www.money.pl/gielda/indeksy_gpw/wig30/'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'
    up_icon = u'\uf176'
    down_icon = u'\uf175'
    json = False
    update_interval = 60
    red = 'AB4642'
    green = 'A1B56C'

    def parse(self, source):
        soup = BeautifulSoup(source, 'html.parser')
        index_change = soup.select('.tabela td')[3].text
        is_down = index_change[0] == '-'
        content = self.down_icon if is_down else self.up_icon
        content += index_change
        content = 'WIG30: ' + content

        self.foreground = self.red if is_down else self.green

        return content


class WeatherConditions(object):
    def __init__(self, temperature, description):
        self.temperature = temperature
        self.description = description

    def __str__(self):
        return '{} - {}'.format(self.description, self.temperature)

    def __repr__(self):
        return '<WeatherConditions {}>'.format(self)


class InteriaWeather(object):
    def get_weather_for_city(self, city_url):
        source = requests.get(city_url).content

        return self.parse_interia_source(source)

    def parse_interia_source(self, source):
        soup = BeautifulSoup(source, 'html.parser')

        current_icon = soup.select('.weather-currently-icon')[0]
        current_condition_description = current_icon['title']
        current_temperature = soup.select('.weather-currently-temp-strict')[0].text

        tomorrow_icon = soup.select('#weather-currently-icon-picture-0')[0]
        tomorrow_condition_description = tomorrow_icon['title']
        tomorrow_temperature = soup.select('#weather-currently-middle-forecast-temperature-max-0')[0].text

        return (
            WeatherConditions(current_temperature, current_condition_description),
            WeatherConditions(tomorrow_temperature, tomorrow_condition_description),
        )


class InteriaWeatherWidget(GenPollUrl):
    SUN = ''
    MOON = ''
    RAIN = ''
    CLOUDY = ''

    icon_for_condition = {
        u'Bezchmurnie': lambda: InteriaWeatherWidget.SUN if 6 < datetime.now().hour < 20 else InteriaWeatherWidget.MOON,
        u'Częściowo słonecznie i burze z piorunami': lambda: InteriaWeatherWidget.RAIN,
        u'Deszcz': lambda: InteriaWeatherWidget.RAIN,
        u'Częściowo słonecznie': lambda: InteriaWeatherWidget.CLOUDY,
        u'Zachmurzenie umiarkowane': lambda: InteriaWeatherWidget.CLOUDY,
        u'Zachmurzenie duże': lambda: InteriaWeatherWidget.CLOUDY,
        u'Słonecznie': lambda: InteriaWeatherWidget.SUN,
        u'Przeważnie słonecznie': lambda: InteriaWeatherWidget.SUN,
        u'Częściowo słonecznie z przelotnymi opadami': lambda: InteriaWeatherWidget.RAIN,
        u'Zachmurzenie duże z przelotnymi opadami': lambda: InteriaWeatherWidget.RAIN,
        u'Zachmurzenie duże i burze z piorunami': lambda: InteriaWeatherWidget.RAIN,
        u'Pochmurno': lambda: InteriaWeatherWidget.CLOUDY,
        u'Przejściowe zachmurzenie': lambda: InteriaWeatherWidget.CLOUDY + '/' + InteriaWeatherWidget.SUN,
    }

    url = 'https://pogoda.interia.pl/prognoza-szczegolowa-wroclaw,cId,39240'
    json = False
    update_interval = 300

    def parse(self, source):
        interia_weather = InteriaWeather()
        current_conditions, tomorrow_conditions = interia_weather.parse_interia_source(source)

        return 'Now: {} Tomorrow: {}'.format(self._format_conditions(current_conditions),
                                             self._format_conditions(tomorrow_conditions))

    def _get_icon_for_conditions(self, conditions):
        description = conditions.description
        return self.icon_for_condition[description]() if description in self.icon_for_condition else description

    def _format_conditions(self, conditions):
        icon = self._get_icon_for_conditions(conditions)
        return '{} {}'.format(icon, conditions.temperature)


ALT = 'mod1'
WIN = 'mod4'
TAB = 'Tab'
CTRL = 'control'
SHIFT = 'shift'
RETURN = 'Return'
SPACE = 'space'
mod = WIN

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
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
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
    Key([mod], "Return", lazy.spawn("gnome-terminal")),
    Key([WIN], "l", lazy.spawn('xlock')),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([CTRL, mod], "j", lazy.next_screen()),
    Key([CTRL, mod], "k", lazy.prev_screen()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

groups = [
    Group('a', spawn='spotify'),
    Group('s', spawn=['xfce4-terminal', 'firefox']),
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
    layout.Stack(num_stacks=2)
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
                widget.Backlight(backlight_name='intel_backlight'),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
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
                InteriaWeatherWidget(),
                widget.TextBox(u' '),
                widget.Battery(charge_char=u'', discharge_char=u'', format='{char} {percent:2.0%}'),
                widget.TextBox(u' '),
                widget.TextBox(u''),
                widget.Volume(foreground='#18BAEB'),
                widget.TextBox(u' '),
                Wig30Widget(),
                widget.TextBox(u' '),
                widget.Clock(format='%Y-%m-%d %a %H:%M'),
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
    subprocess.Popen('xrandr --output HDMI1 --mode 1920x1080 --pos 0x0 --rotate normal --output LVDS1 --primary --mode 1920x1080 --pos 1920x0 --rotate normal --output VIRTUAL1 --off --output DP1 --off --output VGA1 --off'.split())
    subprocess.Popen(['xbindkeys'])
    lazy.restart()()

@hook.subscribe.screen_change
def restart_on_randr(qtile, ev):
    qtile.cmd_restart()
