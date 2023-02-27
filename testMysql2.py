import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:chey0720@127.0.0.1:3306/shop')
query = """select * from goods;"""
goods = pd.read_sql(query, con=engine)

print(goods.head())

import seaborn as sns

iris = sns.load_dataset('iris')
iris.to_sql(name='iris', con=engine, index = False, if_exists='replace')

# 엔진 종료
engine.dispose()
