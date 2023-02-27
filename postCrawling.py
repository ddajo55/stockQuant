import requests as rq
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://kind.krx.co.kr/disclosure/todaydisclosure.do'
payload = {
    'method': 'searchTodayDisclosureSub',
    'currentPageSize': '15',
    'pageIndex': '1',
    'orderMode': '0',
    'orderStat': 'D',
    'forward': 'todaydisclosure_sub',
    'chose': 'S',
    'todayFlag': 'N',
    'selDate': '2023-02-27'
}

data = rq.post(url, data=payload)
# BeautifulSoup을 통해 파싱
html = BeautifulSoup(data.content, 'html.parser')

# prettify함수를 이용해 BeautifulSoup에서 파싱한 파서 트리를 유니코드 형태로 다시 돌려준다
tbl = pd.read_html(html.prettify())
print(type(tbl[0]))