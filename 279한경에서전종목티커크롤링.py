import time
import datetime
import numpy as np

import requests as rq
import pandas as pd

import pymysql

rq.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

market = ['nyse', 'nasdaq', 'amex']
stock_list = []

for i in market:
    url = f'https://www.hankyung.com/globalmarket/data/price?type={i}&sort=market_cap_top&sector_nm=&industry_nm=&chg_net_text='
    data = rq.get(url, verify=False).json()

    data_pd = pd.json_normalize(data['list'])
    data_pd['symbol'] = data_pd['symbol'].str.replace('-US', '')
    data_pd['symbol'] = data_pd['symbol'].str.replace('.', '-')

    stock_list.append(data_pd)

    time.sleep(2)

stock_list_bind = pd.concat(stock_list)
stock_list_bind = stock_list_bind[['hname', 'symbol', 'primary_exchange_name', 'sector_nm', 'market_cap']]
stock_list_bind.rename(columns={'hname': 'Name', 'symbol': 'Symbol', 'primary_exchange_name': 'Exchange', 'sector_nm': 'Sector', 'market_cap': 'MarketCap'}, inplace=True)
stock_list_bind['country'] = 'United States'
stock_list_bind['date'] = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
stock_list_bind = stock_list_bind.drop_duplicates('Symbol')
stock_list_bind.reset_index(inplace=True, drop=True)
stock_list_bind = stock_list_bind.replace({np.nan: None})

con = pymysql.connect(user='root',
                      password='chey0720',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')
mycursor = con.cursor()
query = '''
    insert into global_ticker (Name, Symbol, Exchange, Sector, MarketCap, country, date)
    values (%s, %s, %s, %s, %s, %s, %s) as new
    on duplicate key update
    Name = new.Name, Exchange = new.Exchange, Sector = new.Sector, MarketCap = new.MarketCap;
'''

args = stock_list_bind.values.tolist()
mycursor.executemany(query, args)
con.commit()

con.close()

print(stock_list_bind)