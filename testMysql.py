import pymysql

con = pymysql.connect(
    user = 'root',
    password='chey0720',
    host='127.0.0.1',
    db='shop',
    charset='utf8'
)

myCursor = con.cursor()
query = """
    select * from goods;
"""

myCursor.execute(query)
data = myCursor.fetchall()

query = """
    insert into goods (goods_id, goods_name, goods_classify, sell_price, buy_price, register_date)
    values ('0009', '스테이플러', '사무용품', '2000', '1500', '2020-12-30');
"""

myCursor.execute(query)
con.commit()
con.close()

print(data)