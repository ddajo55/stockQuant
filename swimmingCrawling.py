import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PyKakao import Message
from bs4 import BeautifulSoup

#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver = webdriver.Chrome(ChromeDriverManager().install())
url = "http://stadium.seogwiposports.org/sub03/sub02.php"
driver.get(url)


# 창 최대화
driver.maximize_window()

# 로그인하기
driver.find_element(By.LINK_TEXT, value="로그인").click()
driver.find_element(By.ID, value="login_id").send_keys("dodo7574")
driver.find_element(By.ID, value="login_pw").send_keys("bhey0720")
driver.find_element(By.CLASS_NAME, value="fl_ipt_login").send_keys(Keys.ENTER)

# 로딩시간 기다리기
driver.implicitly_wait(60)

# 제주혁신도시 복합혁신센터 수영장  강좌신청 들어가기
driver.find_element(By.XPATH, value="//*[@id='gnb']/li[4]").click()

numbers = driver.find_elements(By.CLASS_NAME, value="txt_ct")
for i in numbers:
    num = re.findall("\d+/\d+", i.text)
    if len(num) != 0:
        print(num[0].split("/")[1])
# 로딩시간 기다리기
driver.implicitly_wait(60)
# 초급새벽반
driver.find_element(By.XPATH, value="//*[@id='fboardlist']/div/table/tbody/tr[5]/td[1]/h2/a").click()
# 로딩시간 기다리기
driver.implicitly_wait(60)
# 접수신청 버튼 클릭
driver.find_element(By.CLASS_NAME, value="btn_submit").click()
# 로딩시간 기다리기
driver.implicitly_wait(60)

# 접수신청 버튼 클릭 후 경고창이 떴는지 확인
try:
    cnt = 0
    resultAlert = driver.switch_to.alert
    while resultAlert:
        # 로딩시간 기다리기
        driver.implicitly_wait(300)
        resultAlert = driver.switch_to.alert
        print(resultAlert.text)
        resultAlert.accept()
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, value="btn_submit").click()
        cnt += 1
        print(cnt)

    # 경고창 확인버튼 누르기
    #print(resultAlert.accept())

    # 경고창 끄기
    #resultAlert.dismiss()
except:
    print("알림창이 없음===================================")

# 로딩시간 기다리기
driver.implicitly_wait(500)

driver.find_element(By.ID, value="birth").send_keys("19761028")
driver.find_element(By.ID, value="agree").click()
driver.find_element(By.ID, value="captcha_key").click()

# Explicitly wait
wait = WebDriverWait(driver, 200)
element = wait.until(EC.element_to_be_clickable(By.CLASS_NAME, "btn_submit"))
time.sleep(2)

# 카카오톡 메시지 설정
import kakaoMessage
api = Message(service_key="REST API 키")
authUrl = api.get_url_for_generating_code()
print("authUrl : ", authUrl)

# 알림창의 메시지를 카카오톡으로 전송
kakaoMessage.sendKakaoMessage(driver.switch_to.alert.text)
