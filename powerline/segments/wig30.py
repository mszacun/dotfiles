from __future__ import (unicode_literals, division, absolute_import, print_function)
from powerline.lib.threaded import ThreadedSegment
import urllib2
import re

WIG30_URL = "http://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG30"

class Wig30Segment(ThreadedSegment):
	interval = 60
	up_icon = '\uf176'
	down_icon = '\uf175'

	def update(self, old_value):
		page = urllib2.urlopen(WIG30_URL)
		source = page.read()

		match = re.search(r'''<span class="value">(.*?)</''', source)
		index_change = match.groups()[0]

		return index_change

	def render(self, index_change, **kwargs):
		is_down = index_change[0] == '-'
		content = self.down_icon if is_down else self.up_icon
		content +=  index_change

		return [{'contents': content, 'highlight_groups': ['down'] if is_down else ['up']}]

wig30 = Wig30Segment()
