# TradingView Technical Analysis Script

A Python script for automated technical analysis using TradingView data across multiple timeframes.

一個使用 TradingView 數據進行多時間框架自動化技術分析的 Python 腳本。

## Overview / 概述

This script performs comprehensive technical analysis on cryptocurrency trading pairs (specifically BTCUSDTPERP) using the `tradingview_ta` library. It analyzes multiple timeframes and provides both simple and weighted buy/sell signals.

此腳本使用 `tradingview_ta` 函式庫對加密貨幣交易對（特別是 BTCUSDTPERP）進行全面的技術分析。它分析多個時間框架並提供簡單和加權的買入/賣出信號。

## Features / 功能特點

- Multi-timeframe analysis (1m to 1d)
- Technical indicators monitoring (RSI, EMA, MACD, Bollinger Bands, etc.)
- Weighted signal calculation
- Chinese language output support
- Multiple symbol analysis capability

## Dependencies / 依賴項

```python
from tradingview_ta import TA_Handler, Interval, Exchange
import pandas as pd
import config
```

## Main Script / 主要腳本

```python
from tradingview_ta import TA_Handler, Interval, Exchange
# import tradingview_ta
# import time
import pandas as pd
import config

q_symbol = "BTCUSDTPERP"

symbol = config.q_list['{}'.format(q_symbol)]['symbol']
screener = config.q_list['{}'.format(q_symbol)]['screener']
exchange = config.q_list['{}'.format(q_symbol)]['exchange']

interval_list = [Interval.INTERVAL_1_MINUTE,
    Interval.INTERVAL_5_MINUTES,
    Interval.INTERVAL_15_MINUTES,
    Interval.INTERVAL_30_MINUTES,
    Interval.INTERVAL_1_HOUR,
    Interval.INTERVAL_2_HOURS,
    Interval.INTERVAL_4_HOURS,
    Interval.INTERVAL_1_DAY,
   # Interval.INTERVAL_1_WEEK,
   # Interval.INTERVAL_1_MONTH
    ]

sell = 0
buy = 0

# pd.set_option('display.float_format', '{:.2f}'.format)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

day_high = TA_Handler(symbol=symbol, screener=screener, exchange=exchange, interval=Interval.INTERVAL_1_DAY).get_analysis().indicators['high']

for interval in interval_list: 
    handler = TA_Handler(
        symbol=symbol,
        screener=screener,
        exchange=exchange,
        interval=interval
    )
    summary = handler.get_analysis().summary
    oscillators  = handler.get_analysis().oscillators
    moving_averages = handler.get_analysis().moving_averages
    indicators  = handler.get_analysis().indicators 

    msg =       "在{}時間段裏, BUY!! 訊號為{}個, SELL!! 訊號為{}個。\n\
                RSI為:{} || EMA20為: {} || EMA50為: {} || EMA200為: {} \n\
                保力加通度為: {} - {} || 動量指標為: {} || MACD為: {} \n\
                現時K線高低價位為: {} - {}, 波動幅度為: {}, 波動百份比為日線: {}% \n\
                本K線現時成交量為: {}\n\n".format(
                                            interval, 
                                            summary['BUY'],
                                            summary['SELL'],  
                                            round(indicators['RSI'], 2),           
                                            round(indicators['EMA20'], 2), 
                                            round(indicators['EMA50'], 2),
                                            round(indicators['EMA200'], 2),
                                            round(indicators['BB.lower'], 2),
                                            round(indicators['BB.upper'], 2),
                                            round(indicators['Mom'], 2),
                                            round(indicators['MACD.macd'], 2),
                                            round(indicators['low'], 2),
                                            round(indicators['high'], 2),
                                            round((indicators['high']-indicators['low']), 2),
                                            round(((indicators['high']-indicators['low'])/day_high)*100, 2),
                                            round(indicators['volume'], 2),                          
                                            )

    print (msg)

    # # 拿所有的數據, 在不同的時段
    # result_list = [summary, 
    #                 oscillators, 
    #                 moving_averages
    #                 ]

    # for result in result_list:
    #     print(result)
    #    # print('\n')
    
    #print(oscillators)
    buy += summary['BUY']
    sell += summary['SELL']

print ('\n\n所有時間段的分析後得出: 買 = {}, 沽 = {}\n\n\n'.format(buy, sell))

# 列出所有indicator, 在不同的時段
#df = pd.DataFrame(list(indicators.items()), columns  = ['Indicator', 'Value'])
#print(df)
```

## Weighted Signal Analysis / 加權信號分析

```python
# 加權買賣訊號
for interval in interval_list: 
    handler = TA_Handler(
        symbol=symbol,
        screener=screener,
        exchange=exchange,
        interval=interval
    )
    summary = handler.get_analysis().summary
    
    if interval == "1m":
        buy += summary['BUY']
        sell += summary['SELL']
    elif interval == "5m":
        buy += (summary['BUY'] * 2)
        sell += (summary['SELL'] * 2)
    elif interval == "15m":
        buy += (summary['BUY'] * 4)
        sell += (summary['SELL'] * 4)
    elif interval == "30m":
        buy += (summary['BUY'] * 8)
        sell += (summary['SELL'] * 8)
    elif interval == "1h":
        buy += (summary['BUY'] * 16)
        sell += (summary['SELL'] * 16)
    elif interval == "2h":
        buy += (summary['BUY'] * 32)
        sell += (summary['SELL'] * 32)
    elif interval == "4h":
        buy += (summary['BUY'] * 64)
        sell += (summary['SELL'] * 64)
    elif interval == "1d":
        buy += (summary['BUY'] * 128)
        sell += (summary['SELL'] * 128)
    #print (interval, summary)

print ('\n\n所有時間段的分析後得出(加權): 買 = {}, 沽 = {}\n\n\n'.format(buy, sell))
```

## Multiple Symbol Analysis / 多符號分析

```python
from tradingview_ta import *
analysis = get_multiple_analysis(screener="america", interval=Interval.INTERVAL_1_HOUR, symbols=["nasdaq:tsla", "nyse:docn", "nasdaq:aapl"])
print(analysis)
```

## Technical Indicators Monitored / 監控的技術指標

The script monitors the following technical indicators:

- **RSI (Relative Strength Index)** - 相對強弱指數
- **EMA (Exponential Moving Averages)** - 指數移動平均線 (20, 50, 200)
- **Bollinger Bands** - 布林帶 (保力加通度)
- **Momentum** - 動量指標
- **MACD** - 移動平均收斂散度
- **Volume** - 成交量
- **High/Low** - 高低價位

## Weighting System / 加權系統

The script applies different weights to different timeframes:

| Timeframe | Weight | 時間框架 | 權重 |
|-----------|--------|----------|------|
| 1 minute  | 1      | 1分鐘    | 1    |
| 5 minutes | 2      | 5分鐘    | 2    |
| 15 minutes| 4      | 15分鐘   | 4    |
| 30 minutes| 8      | 30分鐘   | 8    |
| 1 hour    | 16     | 1小時    | 16   |
| 2 hours   | 32     | 2小時    | 32   |
| 4 hours   | 64     | 4小時    | 64   |
| 1 day     | 128    | 1天      | 128  |

## Configuration Requirements / 配置要求

The script requires a `config.py` file with the following structure:

```python
q_list = {
    'BTCUSDTPERP': {
        'symbol': 'BTCUSDTPERP',
        'screener': 'crypto',
        'exchange': 'BINANCE'
    }
    # Add more symbols as needed
}
```

## Usage / 使用方法

1. Install required dependencies
2. Configure your symbols in `config.py`
3. Run the script to get technical analysis across multiple timeframes
4. Review both simple and weighted buy/sell signals

## Output Format / 輸出格式

The script provides detailed analysis for each timeframe including:
- Buy/Sell signal counts
- Technical indicator values
- Price range and volatility
- Volume information
- Weighted analysis summary
