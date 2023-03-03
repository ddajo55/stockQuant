from sqlalchemy import create_engine
import pandas as pd
from dateutil.relativedelta import relativedelta
from io import BytesIO
from datetime import date
import requests as rq
from io import BytesIO
import re

engine = create_engine('mysql+pymysql://root:chey0720@127.0.0.1:3306/stock_db')
query = '''
   SELECT * FROM kor_ticker 
    WHERE 기준일 = (SELECT max(기준일) FROM kor_ticker)
    AND 종목구분 = '보통주' 
'''

ticker_list = pd.read_sql(query, con=engine)
print(ticker_list.head())

i = 0
ticker = ticker_list['종목코드'][i]
fr = (date.today() + relativedelta(years=-20)).strftime(('%Y%m%d'))
to = (date.today().strftime('%Y%m%d'))
#print(to, fr)

url = f'https://api.finance.naver.com/siseJson.naver?symbol={ticker}&requestType=1&startTime={fr}&endTime={to}&timeframe=day'

data = rq.get(url).content
data_price = pd.read_csv(BytesIO(data))
print(data_price.count)

# 데이터 클리닝
print('----------------------------------------------------')
price = data_price.iloc[:, 0:6]
price.columns = ['날짜', '시가', '고가', '저가', '종가', '거래량']
price = price.dropna()
price['날짜'] = price['날짜'].str.extract('(\d+)')
price['날짜'] = pd.to_datetime(price['날짜'])
price['종목코드'] = ticker
print(price)

