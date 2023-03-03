import requests as rq
from io import BytesIO
import pandas as pd

gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
gen_otp_stk = {
    'mktId': 'STK',   # KOSPI
    'trdDd': '20230224',
    'money': '1',
    'csvxls_isNo': 'false',
    'name': 'fileDown',
    'url': 'dbms/MDC/STAT/standard/MDCSTAT03901'
}

headers = {'Referer': 'https://http://data.krx.co.kr/contents/MDC/MDI/mdiLoader'}
otp_stk = rq.post(gen_otp_url, gen_otp_stk, headers=headers).text
#print(otp_stk)

down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
down_sector_stk = rq.post(down_url, {'code': otp_stk}, headers=headers)
# 받은 데이터의 content부분을 BytesIO()를 이용해 바이너리 스트림 형태로 만든다.
sector_stk = pd.read_csv(BytesIO(down_sector_stk.content), encoding='EUC-KR')

#print(sector_stk.head())

# 코스닥 다운받기
gen_otp_ksq = {
    'mktId': 'KSQ',  # KOSDAK
    'trdDd': '20230224',
    'money': '1',
    'csvxls_isNo': 'false',
    'name': 'fileDown',
    'url': 'dbms/MDC/STAT/standard/MDCSTAT03901'
}
otp_ksq = rq.post(gen_otp_url, gen_otp_ksq, headers=headers).text

down_sector_ksq = rq.post(down_url, {'code': otp_ksq}, headers=headers)
sector_ksq = pd.read_csv(BytesIO(down_sector_ksq.content), encoding='EUC-KR')

#print(sector_ksq.head())

# 코스피 데이터와 코스닥 데이터를 하나로 합친다
krx_sector = pd.concat([sector_stk, sector_ksq]).reset_index(drop=True)
krx_sector['종목명'] = krx_sector['종목명'].str.strip()
krx_sector['기준일'] = '20230224'

print(krx_sector)
