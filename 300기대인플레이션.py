import matplotlib.pyplot as plt
import pandas_datareader as web
import pandas as pd

# 기대인플레이션 = 10년물 미국 국채 금리 - 10년물 물가연동국채(TIPS) 금리
bei = web.DataReader('T10YIE', 'fred', start='1990-01-01')

bei.plot(figsize=(10, 6), grid=True)
plt.axhline(y=2, color='r', linestyle='-')

plt.show()