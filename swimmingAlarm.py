import re
import kakaoMessage
from datetime import datetime

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

# 카카오톡 메시지 설정
api = Message(service_key="REST API 키")
authUrl = api.get_url_for_generating_code()
print("authUrl : ", authUrl)

while True:
    #driver.refresh()
    # 제주혁신도시 복합혁신센터 수영장  강좌신청 클릭
    driver.find_element(By.XPATH, value="//*[@id='gnb']/li[4]").click()
    # 로딩시간 기다리기
    driver.implicitly_wait(60)

    numbers = driver.find_elements(By.CLASS_NAME, value="txt_ct")
    for i in numbers:
        num = re.findall("\d+/\d+", i.text)
        if len(num) != 0:
            numCount1 = int(num[0].split("/")[0])
            numCount2 = int(num[0].split("/")[1])
            print('numCount1 : ', numCount1, ', munCount2 : ', numCount2)

            # 알림창의 메시지를 카카오톡으로 전송
            if (numCount1 < 20) | (numCount2 < 5):
                print("메시지를 전송합니다")
                msg = "정원 : " + str(numCount1) + ", 초과인원 : " + str(numCount2)
                print(msg)
                kakaoMessage.sendKakaoMessage(msg)
            else:
                print("정원 : ", numCount1, ", 초과인원 : ", numCount2)
    print("-----------------------------------------------------")
    #dateTime = datetime.now()
    nowTime = datetime.now()
    print(nowTime.strftime("%H시 %M분 %S초"))
    print("-----------------------------------------------------")
    time.sleep(10)
