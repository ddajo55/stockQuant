import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url='https://edition.cnn.com/markets/fear-and-greed')
idx = driver.find_element(By.CLASS_NAME, value='market-fng-gauge__dial-number-value').text

driver.close()
idx = int(idx)
print(idx)