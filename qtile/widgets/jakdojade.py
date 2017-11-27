# -*- coding: utf-8 -*-
from time import sleep
from datetime import datetime, date

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from webium import BasePage, Find, Finds

from libqtile.widget.base import ThreadedPollText


class RoutePropositionWidget(WebElement):
    departure_time = Find(by=By.CSS_SELECTOR, value='.cn-time-container')


class JakDojadePage(BasePage):
    url = 'https://jakdojade.pl/wroclaw/trasa/'

    from_field = Find(by=By.CSS_SELECTOR, value='.cn-direction-a input')
    to_field = Find(by=By.CSS_SELECTOR, value='.cn-direction-b input')
    find_routes = Find(by=By.CSS_SELECTOR, value='#cn-planner button.cn-planner-action-button')

    header = Find(by=By.CSS_SELECTOR, value='header')

    routes = Finds(RoutePropositionWidget, By.CSS_SELECTOR, value='.cn-planner-routes-results')


class JakDojadeChecker:
    def check_jakdojade(self, start, destination):
        driver = self._driver()
        page = JakDojadePage(driver=driver)
        page.open()
        sleep(5)
        self._search_for_routes(page, start, destination)
        result = self._get_next_tram_time(page)
        driver.close()
        if result:
            return datetime.combine(date.today(), datetime.strptime(result, '%H:%M').time())
        return None

    def _search_for_routes(self, page, start, destination):
        page.from_field.send_keys(start)
        page.to_field.send_keys(destination)
        page.header.click()
        sleep(5)
        page.find_routes.click()
        sleep(10)

    def _get_next_tram_time(self, page):
        try:
            return page.routes[0].departure_time.text
        except:
            return None

    def _driver(self):
        options = Options()
        options.add_argument('-headless')
        return webdriver.Firefox(firefox_options=options)


class JakDojadeWidget(ThreadedPollText):
    icon = ''
    update_interval = 60

    def __init__(self, start, destination, *args, **kwargs):
        self.start = start
        self.destination = destination
        self.departure_time = datetime(1993, 6, 13)

        super().__init__(*args, **kwargs)

    def poll(self):
        if not self.departure_time or datetime.now() >= self.departure_time:
            self.departure_time = JakDojadeChecker().check_jakdojade(self.start, self.destination)

        formatted = self.departure_time.strftime('%H:%M') if self.departure_time else 'N/A'
        return '{} {}'.format(self.icon, formatted)
