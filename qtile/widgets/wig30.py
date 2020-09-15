from libqtile.widget.generic_poll_text import GenPollUrl
from bs4 import BeautifulSoup


def parse(source):
    soup = BeautifulSoup(source, 'html.parser')
    return soup.select('#boxProfilHeader .change .value')[0].text


class Wig30Widget(GenPollUrl):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'
    up_icon = u'\uf176'
    down_icon = u'\uf175'
    json = False
    update_interval = 60
    red = 'AB4642'
    green = 'A1B56C'

    def __init__(self, index_name, *args, **kwargs):
        self.url = 'https://www.bankier.pl/inwestowanie/profile/quote.html?symbol={}'.format(index_name)
        self.index_name = index_name

        super().__init__(*args, **kwargs)

    def parse(self, source):
        index_change = parse(source)
        is_down = index_change[0] == '-'
        content = self.down_icon if is_down else self.up_icon
        content += index_change
        content = self.index_name + ': ' + content

        self.foreground = self.red if is_down else self.green

        return content
