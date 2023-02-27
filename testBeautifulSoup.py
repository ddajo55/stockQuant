import requests as rq
from bs4 import BeautifulSoup

url = 'https://news.daum.net/economic#1'
data = rq.get(url)
html = BeautifulSoup(data.content, 'html.parser')
html_select = html.select('li > strong.tit_g > a.link_txt')
print([i.get_text() for i in html_select])