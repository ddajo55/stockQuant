import pandas as pd

url = 'https://www.narastat.kr/metasvc/index.do'
tbl = pd.read_html(url)

print(tbl)