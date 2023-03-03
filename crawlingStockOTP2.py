import requests
from io import BytesIO
import pandas as pd
import crawlingStockOPT as crawl
import numpy as np

gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
gen_otp_data = {
    'searchType': '1',
    'mktId': 'ALL',
    'trdDd': '20230224',
    'csvxls_isNo': 'false',
    'name': 'fileDown',
    'url': 'dbms/MDC/STAT/standard/MDCSTAT03501'
}
headers = {'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader'}
otp = requests.post(gen_otp_url, gen_otp_data, headers=headers).text

down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
krx_ind = requests.post(down_url, {'code': otp}, headers=headers)

krx_ind = pd.read_csv(BytesIO(krx_ind.content), encoding='EUC-KR')
krx_ind['종목명'] = krx_ind['종목명'].str.strip()
krx_ind['기준일'] = '20230224'
print(krx_ind.head())

diff = list(set(crawl.krx_sector['종목명']).symmetric_difference(set(krx_ind['종목명'])))

kor_ticker = pd.merge(crawl.krx_sector, krx_ind, on=crawl.krx_sector.columns.intersection(krx_ind.columns).tolist(), how='outer')

#print(kor_ticker.head())
print(kor_ticker[kor_ticker['종목명'].str.contains(r'스펙제[0-9]+호')]['종목명'].values)

# 종목코드 끝자리가 0으로 끝나는 종목은 우선주
print(kor_ticker[kor_ticker['종목코드'].str[-1:] != '0']['종목명'].values)

print(kor_ticker[kor_ticker['종목명'].str.endswith('리츠')]['종목명'].values)

kor_ticker['종목구분'] = np.where(kor_ticker['종목명'].str.contains('스펙제[0-9]+호'), '스펙',
                              np.where(kor_ticker['종목코드'].str[-1:] != '0', '우선주',
                                       np.where(kor_ticker['종목명'].str.endswith('리츠'), '리츠',
                                                np.where(kor_ticker['종목명'].isin(diff), '기타',
                                                         '보통주'))))
# kor_ticker['종목구분'] = 'None'
# kor_ticker['종목구분'] = kor_ticker['종목구분'].where(kor_ticker['종목명'].str.contains('스펙제[0-9]+호'), '스펙')
# kor_ticker['종목구분'].where(kor_ticker['종목명'].str.endswith('리츠'), '리츠')
# kor_ticker['종목구분'].where(kor_ticker['종목명'].isin(diff), '기타')
# kor_ticker['종목구분'].where(kor_ticker['종목명'].str[-1:] != '0', '우선주')
# kor_ticker['종목구분'].where(kor_ticker['종목명'].str[-1:] == '0', '보통주')

kor_ticker = kor_ticker.reset_index(drop=True)
kor_ticker.columns = kor_ticker.columns.str.replace(' ','')
kor_ticker = kor_ticker[['종목코드', '종목명', '시장구분', '종가', '시가총액',
                                 '기준일', 'EPS', '선행EPS', 'BPS', '주당배당금', '종목구분']]
kor_ticker = kor_ticker.replace({np.nan: None})

print(kor_ticker.head())
#print(kor_ticker[kor_ticker['종목명'].str.endswith('리츠')])
# kor_ticker['기준일'] = pd.to_datetime(kor_ticker['기준일'])
# kor_ticker['종가'] = pd.to_numeric(kor_ticker['종가'])
# kor_ticker['시가총액'] = pd.to_datetime(kor_ticker['시가총액'])
# kor_ticker['EPS'] = pd.to_numeric(kor_ticker['EPS'])
# kor_ticker['선행EPS'] = pd.to_numeric(kor_ticker['선행EPS'])
# kor_ticker['BPS'] = pd.to_numeric(kor_ticker['BPS'])
# kor_ticker['주당배당금'] = pd.to_numeric(kor_ticker['주당배당금'])
# kor_ticker['종목명'] = kor_ticker['종목명'].to_string()
# kor_ticker['종목구분'] = kor_ticker['종목구분'].to_string()
# kor_ticker['시장구분'] = kor_ticker['시장구분'].to_string()
# kor_ticker['종목코드'] = kor_ticker['종목코드'].to_string()
print('---------------------------')
kor_ticker = kor_ticker.fillna(0)
print(kor_ticker[kor_ticker['EPS'].isnull()])
print(type(kor_ticker['종목명'].to_string()))
print(kor_ticker.info())
print(kor_ticker.values.tolist()[0])
