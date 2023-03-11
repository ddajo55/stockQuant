import keyring
import requests as rq
from io import BytesIO
import zipfile

import xmltodict
import json
import pandas as pd

import pymysql
from sqlalchemy import create_engine

dart_api_key = '8a205bd0960fe593ecb6b2126d201fd21cb95e7e'
keyring.set_password(dart_api_key, 'dodo7574@gmail.com', 'bhey!0720')

api_key = keyring.get_password(dart_api_key, 'dodo7574@gmail.com')
codezip_url = f'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={dart_api_key}'
codezip_data = rq.get(codezip_url)
codezip_data.headers['Content-Disposition']

# 위에서 받아온 zip파일을 압축 해제
codezip_file = zipfile.ZipFile(BytesIO(codezip_data.content))
codezip_file.namelist()

code_data = codezip_file.read('CORPCODE.xml').decode('utf-8')
data_odict = xmltodict.parse(code_data)
data_dict = json.loads(json.dumps(data_odict))
data = data_dict.get('result').get('list')
corp_list = pd.DataFrame(data)

# stock_code가 없는 열은 제외
corp_list = corp_list[~corp_list['stock_code'].isin([None])]
corp_list.reset_index(inplace=True, drop=True)

engine = create_engine('mysql+pymysql://root:chey0720@127.0.0.1:3306/stock_db')
corp_list.to_sql(name='dart_code', con=engine, index=True, if_exists='append')