# -*- coding: utf-8 -*-
from datetime import datetime

from libqtile.widget.generic_poll_text import GenPollUrl

from bs4 import BeautifulSoup


class WeatherConditions(object):
    def __init__(self, temperature, description):
        self.temperature = temperature
        self.description = description

    def __str__(self):
        return '{} - {}'.format(self.description, self.temperature)

    def __repr__(self):
        return '<WeatherConditions {}>'.format(self)


class InteriaWeather(object):
    def parse_interia_source(self, source):
        soup = BeautifulSoup(source, 'html.parser')

        current_icon = soup.select('.weather-currently-icon')[0]
        current_condition_description = current_icon['title']
        current_temperature = soup.select('.weather-currently-temp-strict')[0].text

        tomorrow_icon = soup.select('#weather-currently-icon-picture-0')[0]
        tomorrow_condition_description = tomorrow_icon['title']
        tomorrow_temperature = soup.select('#weather-currently-middle-forecast-temperature-max-0')[0].text

        sunset_time = soup.select('.weather-currently-info-sunset')[0].text
        sunrise_time = soup.select('.weather-currently-info-sunrise')[0].text

        return (
            WeatherConditions(current_temperature, current_condition_description),
            WeatherConditions(tomorrow_temperature, tomorrow_condition_description),
            sunset_time,
            sunrise_time,
        )


class InteriaWeatherWidget(GenPollUrl):
    SUN = ''
    MOON = ''
    RAIN = ''
    CLOUDY = ''
    SNOW = ''

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
        u'Deszcz i śnieg': lambda: InteriaWeatherWidget.SNOW,
        u'Przelotne opady': lambda: InteriaWeatherWidget.RAIN,
        u'Zachmurzenie duże z przelotnymi opadami śniegu': lambda: InteriaWeatherWidget.SNOW,
        u'Lekkie opady śniegu': lambda: InteriaWeatherWidget.SNOW,
    }

    url = 'https://pogoda.interia.pl/prognoza-szczegolowa-wroclaw,cId,39240'
    json = False
    update_interval = 300

    def parse(self, source):
        interia_weather = InteriaWeather()
        current_conditions, tomorrow_conditions, sunset_time, sunrise_time = interia_weather.parse_interia_source(source)

        return 'Now: {} Tomorrow: {} Sunset: {}'.format(self._format_conditions(current_conditions),
                                                        self._format_conditions(tomorrow_conditions),
                                                        sunset_time)

    def _get_icon_for_conditions(self, conditions):
        description = conditions.description
        return self.icon_for_condition[description]() if description in self.icon_for_condition else description

    def _format_conditions(self, conditions):
        icon = self._get_icon_for_conditions(conditions)
        return '{} {}'.format(icon, conditions.temperature)
