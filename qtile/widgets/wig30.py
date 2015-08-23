from libqtile.widget.generic_poll_text import GenPollUrl
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