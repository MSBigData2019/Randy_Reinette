import unittest
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

website_prefix = 'https://www.reuters.com/finance/stocks/financial-highlights/'
companies_dict = {'Danone' : 'DANO.PA', 'LVMH': 'LVMH.PA', 'Airbus' : 'AIR.PA'}

def _handle_request_and_get_soup(request_result):
    if request_result.status_code == 200:
        html_doc =  request_result.text
        soup = BeautifulSoup(html_doc,"html.parser")
    return soup

def _create_dataframe():
    columns = ['Company Name','Sales Quarter Ending Dec18','Stock Price','Stock Price Change(%)','Share Owned (%)','Dividend Yield Company','Dividend Yield Industry','Dividend Yield Sector']
    df = pd.DataFrame(columns=columns)
    df.set_index('Company Name')
    return df

def _convert_string_to_float(string):
    degenerate_case = re.search(r'--',string)
    if degenerate_case:
        return string
    if ',' in string:
        return float(string.replace(',','')) 
    else:
        return float(string)

def get_quarter_sale(soup):
    return _convert_string_to_float(soup.find('table').find_all_next('tr')[2].find_all('td')[3].text)

def get_stock_value(soup):
    stock = []
    stock.append(_convert_string_to_float(soup.find('div',class_="sectionQuoteDetail").find_all('span')[1].text.split()[0]))
    match = re.search(r'(\()([\+-])(.*?)(%?\))', soup.find('div',class_="priceChange").find_all('span')[-1].text.split()[0])
    if match:
        stock.append(_convert_string_to_float(match.group(2) + match.group(3)))
    return stock

def get_share_percentage(soup):
    return _convert_string_to_float(soup.find('div',class_="column2").find_all('div',class_='moduleBody')[3].find(class_='data').text.strip('%'))

def get_dividend_yield(soup):
    dividend = []
    for i in range(1,4):
        dividend.append(_convert_string_to_float(soup.find_all('table')[2].find_all_next('tr')[1].find_all('td',string=True)[i].text))
    return dividend

def get_all_info(company_name):
    res = requests.get(website_prefix + companies_dict[company_name])
    soup = _handle_request_and_get_soup(res)
    infos = []
    infos.append(get_quarter_sale(soup))
    infos.extend(get_stock_value(soup))
    infos.append(get_share_percentage(soup))
    infos.extend(get_dividend_yield(soup))
    return infos

def main():
    df = _create_dataframe()
    for company in companies_dict.keys():
        df.loc[company] = [company] + get_all_info(company)
    print(df)
if __name__ == '__main__':
    main()

