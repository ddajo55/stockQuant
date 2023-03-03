import pymysql
import jsonCrawlMysqlSector as jsonSector

con = pymysql.connect(user='root',
                      password='chey0720',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')
mycusor = con.cursor()
query = f'''
    insert into kor_sector (IDX_CD, CMP_CD, CMP_KOR, SEC_NM_KOR, 기준일)
    values (%s, %s, %s, %s, %s) as new
    on duplicate key update
    IDX_CD = new.IDX_CD, CMP_CD = new.CMP_CD, CMP_KOR = new.CMP_KOR, SEC_NM_KOR = new.SEC_NM_KOR
'''

args = jsonSector.kor_sector.values.tolist()

mycusor.executemany(query, args)
con.commit()

con.close()