import time
import json
import requests as rq
import pandas as pd
from tqdm import tqdm

url = 'https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230228&sec_cd=G10'
data = rq.post(url).json()

print(data.keys())
print(data['sector'])
# 섹터코드를 데이터프레임으로 변환하여 추출
sector_code = pd.json_normalize(data['sector'])['SEC_CD'].values

data_sector = []

for i in tqdm(sector_code):
    url = f'https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20230228&sec_cd={i}'
    data = rq.get(url).json()
    data_pd = pd.json_normalize(data['list'])

    data_sector.append(data_pd)
    time.sleep(2)

kor_sector = pd.concat(data_sector, axis=0)
kor_sector = kor_sector[['IDX_CD', 'CMP_CD', 'CMP_KOR', 'SEC_NM_KOR']]
kor_sector['기준일'] = '20230224'
kor_sector['기준일'] = pd.to_datetime(kor_sector['기준일'])
print('------------------------')
print(type(kor_sector.values.tolist()))
print(kor_sector.info())
