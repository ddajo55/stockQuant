import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader as web
import pandas as pd
import yfinance as yf


# 주가지수 다운로드
sp = yf.download('^GSPC', progress=False, start='1990-01-01')
# 장단기금리 다운로드
t10y2y = web.DataReader('T10Y2Y', 'fred', start='1990-01-01')
t10y3m = web.DataReader('T10Y3M', 'fred', start='1990-01-01')

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(t10y2y, color='black', linewidth=0.5, label='10Y-2Y')
ax1.plot(t10y3m, color='red', linewidth=0.5, label='10Y-3M')
ax1.axhline(y=0, color='r', linestyle='dashed')
ax1.legend(loc='lower right')

ax2 = ax1.twinx()
ax2.plot(np.log(sp['Close']), label='S&P500')
ax2.set_ylabel('S&P500 지수(로그)')
ax2.legend(loc='upper right')

plt.show()