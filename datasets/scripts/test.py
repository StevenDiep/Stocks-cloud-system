#The following code gives us stock data from the S&P500 companies for the past
#5 years into a JSON file

import bs4 as bs
import requests
import yfinance as yf
import datetime
import json
from entry_functions import dict_convert
from concurrent import futures


def get_stock(stock_dict, ticker):
    current_ticker = yf.Ticker(ticker)
    hist = current_ticker.history(period="1mo")["Close"]
    current_stock_info = hist.to_dict()
    current_stock_info = dict_convert(current_stock_info)
    
    stock_dict[ticker] = current_stock_info
    
#The following block of code retrieves the tickers of the S&P 500 companies
resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(resp.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})

tickers = []


for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text
    tickers.append(ticker)
tickers = [s.replace('\n', '') for s in tickers]



tickers.insert(0, "^GSPC")

#The following block of code will create our json file that contains our dataset
stocks = {};

results = [(stocks, ticker) for ticker in tickers]

print(results)