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

from tradingview_ta import *
analysis = get_multiple_analysis(screener="america", interval=Interval.INTERVAL_1_HOUR, symbols=["nasdaq:tsla", "nyse:docn", "nasdaq:aapl"])
print(analysis)



