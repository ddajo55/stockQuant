from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import math
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://www.investing.com/stock-screener/?sp=country::5|sector::a|industry::a|equityType::ORD%3Ceq_market_cap;1'
driver.get(url)

html = BeautifulSoup(driver.page_source, 'lxml')
# 국가명 text로 가져오기
country = html.find('input', class_='js-search-input inputDropDown')['value']

print('---------------------'*2)
print(html)

# 종목 데이터 테이블로 가져오기
html_table = html.select('table.genTbl.openTbl.resultsStockScreenerTbl.elpTbl')
# BeautifulSoup에서 파싱한 파서트리를 유니코드 형태로 다시 돌려준다
df_table = pd.read_html(html_table[0].prettify())
df_table_result = df_table[0]

df_table_select = df_table_result[['Name', 'Symbol', 'Exchange', 'Sector', 'Market Cap']]
end_page_num = driver.find_element(By.CLASS_NAME, value='js-total-results').text


driver.quit()
