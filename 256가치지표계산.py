from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# DB 연결
engine = create_engine('mysql+pymysql://root:chey0720@127.0.0.1:3306/stock_db')

# ticker 리스트
ticker_list = pd.read_sql('''
    select * from kor_ticker
    where 기준일 = (select max(기준일) from kor_ticker)
    and 종목구분 = '보통주'
''', con=engine)

# 삼성전자 분기 재무제표
sample_fs = pd.read_sql('''
    select * from kor_fs
    where 공시구분 = 'q'
    and 종목코드 = '005930'
    and 계정 in ('당기순이익', '자본', '영업활동으로인한현금흐름', '매출액');
''', con=engine)

engine.dispose()

sample_fs = sample_fs.sort_values(['종목코드', '계정', '기준일'])
sample_fs['ttm'] = sample_fs.groupby(['종목코드', '계정'], as_index=False)['값'].rolling(window=4, min_periods=4).sum()['값']

# where 함수 : 조건이 만족하면 A 아니면 B
sample_fs['ttm'] = np.where(sample_fs['계정'] == '자본',
                            sample_fs['ttm'] / 4, sample_fs['ttm'])
sample_fs = sample_fs.groupby(['계정', '종목코드']).tail(1)
# sample_fs = sample_fs.dropna(axis=0)

# 재무제표의 경우 단위가 억인데 시가총액만 단위가 원이므로 억으로 나눠준다
sample_fs_merge = sample_fs[['계정', '종목코드', 'ttm']].merge(ticker_list[['종목코드', '시가총액', '기준일']], on='종목코드')
sample_fs_merge['시가총액'] = sample_fs_merge['시가총액'] / 100000000

# 지표 계산하기
sample_fs_merge['value'] = sample_fs_merge['시가총액'] / sample_fs_merge['ttm']
sample_fs_merge['지표'] = np.where(
    sample_fs_merge['계정'] == '매출액', 'PSR',
    np.where(
        sample_fs_merge['계정'] == '영업활동으로인한현금흐름', 'PCR',
        np.where(
            sample_fs_merge['계정'] == '자본', 'PBR',
            np.where(sample_fs_merge['계정'] == '당기순이익', 'PER', None)
        )
    )
)

# 배당 수익률 계산
ticker_list_dividend = ticker_list[ticker_list['종목코드'] == '005930'].copy()
ticker_list_dividend['DY'] = ticker_list_dividend['주당배당금'] / ticker_list_dividend['종가']

print('----------------')
print(ticker_list_dividend)
