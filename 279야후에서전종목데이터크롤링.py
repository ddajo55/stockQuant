import yfinance as yf
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import time
from tqdm import tqdm

# DB 연결
engine = create_engine('mysql+pymysql://root:chey0720@127.0.0.1:3306/stock_db')
con = pymysql.connect(user='root',
                      password='chey0720',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')

mycursor = con.cursor()

price = yf.download('AAPL', progress=False)

# ticker list 불러오기
ticker_list = pd.read_sql('''
   select * from global_ticker
   where date = (select max(date) from global_ticker) 
   and country = 'United Stateｓ'
''', con=engine)

query = '''
    insert into global_price (Date, High, Low, Open, Close, Volume, `Adj Close`, ticker)
    values(%s, %s, %s, %s, %s, %s, %s, %s) as new
    on duplicate key update
    High = new.High, Low = new.Low, Open = new.Open, Close = new.Close, Volume = new.Volume, `Adj Close` = new.`Adj Close`
'''

error_list = []

# 전종목 주가 다운로드 및 저장
for i in tqdm(range(0, len(ticker_list))):
    #티커 선택
    ticker = ticker_list['Symbol'][i]

    # 오류 발생시 이를 무시하고 다음 루프 진행
    try:
        # 주가 다운로드
        price = yf.download(ticker, progress=False)

        # 데이터 클렌징
        price = price.reset_index()
        price['ticker'] = ticker

        # 주가 데이터를 DB에 저장
        args = price.values.tolist()
        mycursor.executemany(query, args)
        con.commit()
    except:
        print(ticker, ' : 오류 발생')
        error_list.append(ticker)

    time.sleep(2)

# DB 연결 종료

print(ticker_list)