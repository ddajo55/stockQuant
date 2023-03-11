import pandas_datareader as web
import pandas as pd
import yfinance as yf
import statsmodels.api as sm

tickers = ['^KS11', '039490.KS']

all_data = {}
for ticker in tickers:
    all_data[ticker] = yf.download(ticker, start='2016-01-01', end='2021-12-31', progress=False)
    print(type(yf.download(ticker, start='2016-01-01', end='2021-12-31', progress=False)))
    # all_data[ticker] = web.DataReader(ticker, 'yahoo', start='2016-01-01', end='2021-12-31')

print('-'*100)
print(all_data.items())

prices = pd.DataFrame({tic: data['Close'] for tic, data, in all_data.items()})
ret = prices.pct_change().dropna()

ret['intercept'] = 1
reg = sm.OLS(ret[['039490.KS']], ret[['^KS11', 'intercept']]).fit()

reg.summary()
print(reg.params)