import json
import requests as rq
import pandas as pd

url = 'https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230228&sec_cd=G10'
data = rq.get(url).json()

print(data.keys())
print(data['list'][0])
print(data['sector'])
data_pd = pd.json_normalize(data['list'])
print('-----------------------------------')
print(data_pd.head())
