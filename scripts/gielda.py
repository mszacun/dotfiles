import sys

import requests
from bs4 import BeautifulSoup

from texttable import Texttable

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

requested_companies = sys.argv[1:]

html = requests.get('https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=WIG').content
soup = BeautifulSoup(html, 'html.parser')
companys_rows = soup.select('table.sortTableMixedData:nth-child(1) > tbody:nth-child(2) tr')


companys = [get_company_from_row(row) for row in companys_rows]
filtered_companys = [company for company in companys if company['name'] in requested_companies]
sorted_by_price_change = sorted(filtered_companys, key=lambda company: parse_percent(company['percent_change']), reverse=True)

table = Texttable()
table.set_deco(Texttable.HEADER)
table.set_cols_dtype(['t', 'f', 'f'])
table.set_cols_align(["l", "r", "r"])
table.header(['Name', 'Current Price', 'Percent Change'])

for company in sorted_by_price_change:
    table.add_row([company['name'], company['price'], company['percent_change']])

print(table.draw())
