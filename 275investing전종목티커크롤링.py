from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import datetime
import math
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import pymysql

driver = webdriver.Chrome(ChromeDriverManager().install())
# 국가번호 5 : USA
nationCode = 5
url = f'https://www.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::ORD%3Ceq_market_cap;1'
driver.get(url)

# 튜플로 XPATH 인수를 전달해야 오류가 발생하지 않음
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="resultsTable"]')))

# 크롤링 할 총 페이지 수 계산
end_page_num = driver.find_element(By.CLASS_NAME, value='js-total-results').text
end_page_num = math.ceil(int(end_page_num) / 50)

all_data_df = []
all_data_err = []

for page in tqdm(range(1, end_page_num + 1)):
# for page in tqdm(range(1, 10)):
    url = f'https://www.investing.com/stock-screener/?sp=country::{nationCode}|sector::a|industry::a|equityType::ORD%3Ceq_market_cap;{page}'
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="resultsTable"]/tbody')))
    except:
        time.sleep(2)
        driver.refresh()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="resultsTable"]/tbody')))
        print('Exception : ========================================================')

    html = BeautifulSoup(driver.page_source, 'lxml')

    html_table = html.select('table.genTbl.openTbl.resultsStockScreenerTbl.elpTbl')

    # BeautifulSoup에서 파싱한 파서트리를 유니코드 형태로 다시 돌려준다
    df_table = pd.read_html(html_table[0].prettify())
    df_table_select = df_table[0][['Name', 'Symbol', 'Exchange', 'Sector', 'Market Cap']]
    all_data_df.append(df_table_select)
    if df_table_select.size <= 0:
        print('page : ', page, ' 데이터가 존재하지 않습니다')
        all_data_err = all_data_err.append(page)

    time.sleep(2)

if len(all_data_err) > 0:
    print('+'*100)
    print('데이터가 없는 페이지 : ', all_data_err)
    print('+'*100)

all_data_df_bind = pd.concat(all_data_df, axis=0)

data_country = html.find(class_='js-search-input inputDropDown')['value']
all_data_df_bind['country'] = data_country
all_data_df_bind['date'] = datetime.datetime.today().strftime('%Y-%m-%d')
# all_data_df_bind['date'] = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
all_data_df_bind = all_data_df_bind[~all_data_df_bind['Name'].isnull()]
all_data_df_bind = all_data_df_bind[all_data_df_bind['Exchange'].isin(['NASDAQ', 'NYSE', 'NYSE Amex'])]
all_data_df_bind = all_data_df_bind.drop_duplicates((['Symbol']))
all_data_df_bind.reset_index(inplace=True, drop=True)
all_data_df_bind = all_data_df_bind.replace({np.nan: None})
all_data_df_bind.rename(columns={'Market Cap': 'MarketCap'}, inplace=True)

print('-' * 100)
print(all_data_df_bind.head())
print(all_data_df_bind.info())

con = pymysql.connect(user='root',
                      password='chey0720',
                      host='127.0.0.1',
                      db='stock_db',
                      charset='utf8')
mycursor = con.cursor()
query = '''
    insert into global_ticker (Name, Symbol, Exchange, Sector, MarketCap, country, date)
    values (%s, %s,%s, %s, %s, %s, %s) as new
    on duplicate key update
    Name = new.Name, Exchange = new.Exchange, Sector = new.Sector, MarketCap = new.MarketCap; 
'''

args = all_data_df_bind.values.tolist()

mycursor.executemany(query, args)
con.commit()

driver.quit()