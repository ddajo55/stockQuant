import requests
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 카카오톡 인증코드 받아오기
driver = webdriver.Chrome(ChromeDriverManager().install())
kakaoUrl = "https://kauth.kakao.com/oauth/authorize?client_id=234e4d47b42787f9d25e3e0152d7636a&redirect_uri=https://www.naver.com/&response_type=code&scope=talk_message"
driver.get(kakaoUrl)

driver.find_element(By.ID, value="loginKey--1").send_keys("ddajo55@hanmail.net")
driver.find_element(By.ID, value="password--2").send_keys("ahey0720")
driver.find_element(By.XPATH, value="//*[@id='mainContent']/div/div/form/div[4]/button[1]").click()
#driver.find_element(By.XPATH, value="//*[@id='agreeAll']").click()
#driver.find_element(By.ID, value="txt_accept_button_agree").click()
time.sleep(2)
currentUrl = driver.current_url.split("code=")[1]
print(currentUrl)

url = "https://kauth.kakao.com/oauth/token"
restApiKey = "234e4d47b42787f9d25e3e0152d7636a"
redirectUri = "https://www.naver.com/"
authorizeKey = currentUrl

data = {
    'grant_type':'authorization_code',
    'client_id':restApiKey,
    'redirect_uri':redirectUri,
    'code': authorizeKey,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# json 저장
#1.
#with open(r"C:\Users\dodo7\Desktop\PythonWorkspace\kakao_test\kakao_code.json","w") as fp:
#    json.dump(tokens, fp)

#2.
with open("kakao_code.json","w") as fp:
    json.dump(tokens, fp)

#################################################

# json 읽어오기
#1.
#with open(r"C:\Users\user\Desktop\PythonWorkspace\kakao_test\kakao_code.json","r") as fp:
#    ts = json.load(fp)
#print(ts)
#print(ts["access_token"])

#2.

##############################################
#2.
with open("kakao_code.json","r") as fp:
    tokens = json.load(fp)
print(tokens)
print(tokens["access_token"])

#url="https://kapi.kakao.com/v2/api/talk/memo/send"
url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

# kapi.kakao.com/v2/api/talk/memo/default/send

headers={
    "Authorization" : "Bearer " + tokens["access_token"]
}

def sendKakaoMessage(msg):
    data = {
           'object_type': 'text',
            "text": msg,
           'link': {
               'web_url': 'https://developers.kakao.com',
               'mobile_web_url': 'https://developers.kakao.com'
           },
           'button_title': '키워드'
       }
    data = {'template_object': json.dumps(data)}
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))