from datetime import date

import pandas as pd
import requests as rq
from dateutil.relativedelta import relativedelta

dart_api_key = '8a205bd0960fe593ecb6b2126d201fd21cb95e7e'

bgn_date = (date.today() + relativedelta(days=-8)).strftime('%Y%m%d')
end_date = date.today().strftime(('%Y%m%d'))

notice_url = f'''https://opendart.fss.or.kr/api/list.json?crtfc_key={dart_api_key}&bgn_de={bgn_date}&end_de={end_date}&page_no=1&page_count=100'''

notice_data = rq.get(notice_url).json()
notice_data_df = notice_data.get('list')
notice_data_df = pd.DataFrame(notice_data_df)

# 삼성전자의 개별 기업 공시데이터만 뽑아오기
bgn_date = (date.today() + relativedelta(days=-30)).strftime('%Y%m%d')
end_date = date.today().strftime('%Y%m%d')
corp_code = '00126380'

notice_url_ss = f'''https://opendart.fss.or.kr/api/list.json?crtfc_key={dart_api_key}&corp_code={corp_code}&bgn_de={bgn_date}&end_de={end_date}&page_no=1&page_count=100'''

notice_data_ss = rq.get(notice_url_ss).json().get('list')
notice_data_ss_df = pd.DataFrame(notice_data_ss)

# rcept_no 공시번호로 해당 데이터를 이용해 공시에 해당하는 URL에 접속하여 내역을 확인
notice_url_exam = notice_data_ss_df.loc[0, 'rcept_no']
notice_dart_url = f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo={notice_url_exam}'

# 배당관련 사항
corp_code = '00126380'
bsns_year = '2021'
reprt_code = '11011'

url_div = f'https://opendart.fss.or.kr/api/alotMatter.json?crtfc_key={dart_api_key}&corp_code={corp_code}&bsns_year={bsns_year}&reprt_code={reprt_code}'
div_data_ss = rq.get(url_div)
div_data_ss_df = div_data_ss.json().get('list')
div_data_ss_df = pd.DataFrame(div_data_ss_df)

print('-'*100)
print(notice_data_df)