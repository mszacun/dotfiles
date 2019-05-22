import sys
import os
import json

import requests
from bs4 import BeautifulSoup

from texttable import Texttable

UP_ARROW = '\033[92m\uf176\033[0m'
DOWN_ARROW = '\033[91m\uf175\033[0m'


PREVIOUS_RUN_FILE_PATH = os.path.join(os.path.expanduser('~/.stocks.json'))


def get_company_from_row(company_row):
    row = company_row.select('td')

    return {
        'name': row[0].text,
        'ticker': row[1].text,
        'price': row[2].text,
        'change': row[3].text,
        'percent_change': row[4].text,
        'index_impact': row[5].text,
        'trade_contribution': row[6].text,
        'shares_number': row[7].text,
        'wallet_contribution': row[8].text,
    }

def parse_percent(percent_str):
    return float(percent_str[:-1].replace(',', '.'))

def get_direction(company, previous_run):
    name = company['name']
    price = float(company['price'].replace(',', '.'))
    previous_price = float(previous_run[name].replace(',', '.'))

    return UP_ARROW if price > previous_price else DOWN_ARROW

requested_companies = sys.argv[1:]

html = requests.get('https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG').content
soup = BeautifulSoup(html, 'html.parser')
companys_rows = soup.select('table.sortTableMixedData:nth-child(1) > tbody:nth-child(2) tr')


companys = [get_company_from_row(row) for row in companys_rows]
filtered_companys = [company for company in companys if company['name'] in requested_companies]
sorted_by_price_change = sorted(filtered_companys, key=lambda company: parse_percent(company['percent_change']), reverse=True)

table = Texttable()
table.set_deco(Texttable.HEADER)
table.set_cols_dtype(['t', 'f', 'f', 't'])
table.set_cols_align(["l", "r", "r", 'c'])
table.header(['Name', 'Current Price', 'Percent Change', 'Direction'])

with open(PREVIOUS_RUN_FILE_PATH, 'r') as f:
    previous_run = json.load(f)

for company in sorted_by_price_change:
    table.add_row([company['name'], company['price'], company['percent_change'], get_direction(company, previous_run)])
    previous_run[company['name']] = company['price']

with open(PREVIOUS_RUN_FILE_PATH, 'w') as f:
    json.dump(previous_run, f, indent=4, sort_keys=True)

print(table.draw())
