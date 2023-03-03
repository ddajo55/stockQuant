from sqlalchemy import create_engine
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import re

engine = create_engine('mysql+pymysql://root:chey0720@127.0.0.1:3306/stock_db')
query = '''
    select * from kor_ticker
    where 기준일 = (select max(기준일) from kor_ticker) and 종목구분 = '보통주';
'''
ticker_list = pd.read_sql(query, con=engine)
engine.dispose()

i = 0
ticker = ticker_list['종목코드'][i]

# url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701'
url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701'
data = pd.read_html(url, displayed_only=False)

print([item.head(3) for item in data])
print('====================================')
# 년간
print(data[0].columns.tolist(), '\n',
      data[2].columns.tolist(), '\n',
      data[4].columns.tolist())
# 분기
print(data[1].columns.tolist(), '\n',
      data[3].columns.tolist(), '\n',
      data[5].columns.tolist())
data_fs_y = pd.concat(
    [data[0].iloc[:, ~data[0].columns.str.contains('전년동기')], data[2], data[4]]
)
data_fs_y = data_fs_y.rename(columns={data_fs_y.columns[0]: '계정'})
print(data_fs_y)

page_data = rq.get(url)
page_data_html = BeautifulSoup(page_data.content, 'html.parser')
fiscal_data = page_data_html.select('div.corp_group1 > h2')
fiscal_data_text = fiscal_data[1].text
fiscal_data_text = re.findall('[0-9]+', fiscal_data_text)

# 결산월에 해당하는 부분만 선택
data_fs_y = data_fs_y.loc[:, (data_fs_y.columns == '계정') | (data_fs_y.columns.str[-2:].isin(fiscal_data_text))]

# 열 이름이 '계정', 그리고 제무제표의 월이 결산월과 같은 부분만 선택
data_clean1 = data_fs_y[data_fs_y.loc[:,~data_fs_y.columns.isin(['계정'])].isna().all(axis=1)]

data_clean2 = data_fs_y['계정'].value_counts(ascending=False)

# 데이터 클렌징 함수
def clean_fs(df, ticker, frequency):
    df = df[~df.loc[:, ~df.columns.isin(['계정'])].isna().all(axis=1)]
    # 중복된 데이터가 있을 경우 첫번째 데이터를 제외한 나머지 삭제
    df = df.drop_duplicates(['계정'], keep='first')
    # melt함수 : DataFrame을 tidy한 데이터로 변환하는 함수
    df = pd.melt(data_fs_y, id_vars='계정', var_name='기준일', value_name='값')
    # 계정값이 없는 항목 삭제
    df = df[~pd.isnull(df['값'])]
    # [계산에 참여한 계정 펼치기] 삭제
    # df = df['계정'] = df['계정'].replace({'계산에 참여한 계정 펼치기': ''}, regex=True)
    df = df[~df['계정'].str.contains('펼치기')]
    # df['기준일'] = pd.to_datetime(df['기준일'], format='%Y-%m') + pd.tseries.offsets.MonthEnd()
    df['종목코드'] = ticker
    df['공시구분'] = frequency

    return df

data_fs_y_clean = clean_fs(data_fs_y, ticker, 'y')

# 분기 데이터
data_fs_q = pd.concat([data[1].loc[:, ~data[1].columns.str.contains('전년동기')], data[3], data[5]])
data_fs_q = data_fs_q.rename(columns={data_fs_q.columns[0]: '계정'})
data_fs_q_clean = clean_fs(data_fs_q, ticker, 'q')

# 년간 분간 합치기
data_fs_bind = pd.concat([data_fs_y_clean, data_fs_q_clean])


print('-------------------------------------')
print(data_fs_y_clean)
print(data_fs_q_clean)
