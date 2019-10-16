import sys
import os
import json

import requests
from bs4 import BeautifulSoup

from texttable import Texttable

UP_ARROW = '\033[92m\uf176\033[0m'
DOWN_ARROW = '\033[91m\uf175\033[0m'


PREVIOUS_RUN_FILE_PATH = os.path.join(os.path.expanduser('~/.stocks.json'))


def parse_percent(percent_str):
    return float(percent_str[:-1].replace(',', '.'))


class QutationTable:
    def __init__(self, url):
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        companys_rows = soup.select('table.sortTableMixedData:nth-child(1) > tbody:nth-child(2) tr')
        self.companys = [self._get_company_from_row(row) for row in companys_rows]

    def _get_company_from_row(self, company_row):
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


class PresentationTable(Texttable):
    def __init__(self, companies, previous_run_data):
        super().__init__()

        self.companies = companies
        self.previous_run_data = previous_run_data

        self.set_deco(Texttable.HEADER)
        self.set_cols_dtype(['t', 'f', 'f', 't'])
        self.set_cols_align(["l", "r", "r", 'c'])
        self.header(['Name', 'Current Price', 'Percent Change', 'Direction'])

        for company in companies:
            direction =  self._get_direction(company, previous_run_data)
            self.add_row([company['name'], company['price'], company['percent_change'], direction])


    def _get_direction(self, company, previous_run):
        name = company['name']
        price = float(company['price'].replace(',', '.'))
        previous_price = float(previous_run.get(name, '0.00').replace(',', '.'))

        return UP_ARROW if price > previous_price else DOWN_ARROW

url = sys.argv[1]
requested_companies = sys.argv[2:]

table = QutationTable(url)

if requested_companies:
    filtered_companys = [company for company in table.companys if company['name'] in requested_companies]
else:
    filtered_companys = table.companys

sorted_by_price_change = sorted(filtered_companys, key=lambda company: parse_percent(company['percent_change']), reverse=True)

with open(PREVIOUS_RUN_FILE_PATH, 'r') as f:
    previous_run_data = json.load(f)

table2 = PresentationTable(sorted_by_price_change, previous_run_data)
print(table2.draw())

previous_run_data.update({company['name']: company['price'] for company in table.companys})

with open(PREVIOUS_RUN_FILE_PATH, 'w') as f:
    json.dump(previous_run_data, f, indent=4, sort_keys=True)

