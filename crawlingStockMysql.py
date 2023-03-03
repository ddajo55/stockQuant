import pymysql
import crawlingStockOTP2 as crawStock

con = pymysql.connect(user='root',
                      password='chey0720',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')
mycursor = con.cursor()
query = f"""
    insert into kor_ticker (종목코드, 종목명, 시장구분, 종가, 시가총액, 기준일, EPS, 선행EPS, BPS, 주당배당금, 종목구분)
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) as new
    on duplicate key update
    종목명=new.종목명, 시장구분=new.시장구분, 종가=new.종가, 시가총액=new.시가총액, EPS=new.EPS, 선행EPS=new.선행EPS, BPS=new.BPS, 주당배당금=new.주당배당금, 종목구분=new.종목구분
"""
print(query)
args = crawStock.kor_ticker.values.tolist()
mycursor.executemany(query, args)
con.commit()

con.close()
