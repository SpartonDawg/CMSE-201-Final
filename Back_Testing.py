import pandas as pd
import datetime
import pandas_datareader
from pandas_datareader import data as web
import matplotlib.pyplot as plt
import datetime
import datetime as dt
import numpy as np
import random
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import PercentFormatter
from scipy.stats import norm
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



sp = eurcsv
close = sp['Price']
date = sp['Date']


returns = ((close[2] - close[1])/close[1])*100
print(close[2])
print(close[1])
print(returns)


def tester(date_in,price_in):
    buys = []
    shorts = []
    rets = []
    s_rets = []
    benchmark = []
    date = pd.to_datetime(date_in)
    twenty_six = pd.ewma(price_in, span=26)
    twelve = pd.ewma(price_in, span=12)
    macd = twelve - twenty_six
    delta_macd = macd.pct_change(periods=2)
    mix = []
    mix_port = []
    print(delta_macd)

    for i in range(len(price_in)-1):
        if macd[i] > 0:
            buys.append(i)
            mix.append(i)
        elif delta_macd[i] < -.15 and macd[i] < -.003:
            shorts.append(i)
            mix.append(i)
    for i in buys:
        j = int(i)
        j1 = int(i+1)
        returns = ((price_in[j1] - price_in[j])/price_in[j])*100
        rets.append(returns)
    for i in shorts:
        s = int(i)
        s1 = int(i+1)
        s_returns = ((price_in[s1] - price_in[s])/price_in[s])*-100
        s_rets.append(s_returns)
#    for i in mix:
#        j = int(i)
#        j1 = int(i+1)
#        mix_return = ((price_in[j1] - price_in[j])/price_in[j])*100
#        mix_port.append(mix_return)        
        
    for i in range(len(price_in)-1):
        z = int(i)
        z1 = int(i+1)
        base = ((price_in[z1] - price_in[z])/price_in[z])*100
        benchmark.append(base)
    plt.plot(np.cumsum(mix_port))
    x_bench = np.linspace(0,1,len(benchmark))
    x_strat = np.linspace(0,1,len(rets))      
    plt.plot(np.cumsum(s_rets))
    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(x_strat, np.cumsum(rets),label="Strategy")
    ax.plot(x_bench, np.cumsum(benchmark),label="Benchmark")
#    ax2 = ax.twinx()
#    ax2.plot(np.linspace(0,1,len(macd)), macd, 'r')
    ax.yaxis.set_major_formatter(PercentFormatter())    
    ax.legend(fontsize=15)
    print("Strategy Return = %",sum(rets))
    print("Total Return Outright = %",sum(benchmark))
    
    #RISK ASSESMENT BENCHMARK
    delta_returns = price_in.pct_change()
    mean_returns = np.mean(delta_returns)
    std_returns = np.std(delta_returns)
    VAR_95 = norm.ppf(1-0.95,mean_returns, std_returns)*100
    print("Benchmark VAR @ confidence Level = 95% Level", VAR_95)
    
    #RISK ASSESMENT STRATEGY
    #delta_returns_strat = price_in.pct_change()
    mean_returns_strat = np.mean(rets)
    std_returns_strat = np.std(rets)
    VAR_95_strat = norm.ppf(1-0.95,mean_returns_strat, std_returns_strat)
    print("Strategy VAR @ confidence Level = 95% Level", VAR_95_strat)
tester(date,close)



twenty_six = pd.ewma(close, span=26)
twelve = pd.ewma(close, span=12)
macd = twelve - twenty_six
date = pd.to_datetime(sp['Date'])
fig, ax1 = plt.subplots(figsize=(13,5))
ax1.plot(date, macd, 'b-')
ax2 = ax1.twinx()
ax2.plot(date, close, 'r')
ax2.set_ylabel(color='r')
ax2.tick_params('y', colors='r')
fig.tight_layout()