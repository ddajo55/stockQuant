from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://root:chey0720@127.0.0.1:3306/shop')
price = pd.DataFrame({
    "날짜": ['2021-01-02', '2021-01-03'],
    "티커": ['000001', '000001'],
    "종가": [1340, 1315],
    "거래량": [1000, 2000]
})

print(price.head())

#price.to_sql(name='price', con=engine, if_exists='append', index=False)
data_sql = pd.read_sql('price', con=engine)

new = pd.DataFrame({
    "날짜": ['2021-01-04'],
    "티커": ['000001'],
    "종가": [1320],
    "거래량": [1500]
})
price = pd.concat([price, new])
price.to_sql(name='price', con=engine, if_exists='append', index=False)
data_sql = pd.read_sql('price', con=engine)
engine.dispose()
print(data_sql.head())
