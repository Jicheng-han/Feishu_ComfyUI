import numpy as np
import pandas as pd
import akshare as ak
import datetime
from urllib import request
import json
 
def get_sina_kline(symbol='m2201', period='d', market='期货',**kwargs) -> 'DataFrame':
    '''
    用途：获取sina股票期货指定周期的人历史1023个数据
    返回：DataFrame  columns name [date,open,high,low,close,volume]
    参数:
    symbol品种代码,
    period是周期(5m,15m,30m,60m日线),datalen是获取数据的长度，最大就是1023
    mode=['股票','期货','股指期货']
    kwargs:仅用于A股
    stock_zh_a_daily(symbol: str = 'sh603843', start_date: str = '19900101', end_date: str = '21000118', adjust: str = '') ->‘DataFrame’
    start_date: str = '19900101',
    end_date: str = '21000118',
    adjust: str = '' 默认为空: 返回不复权的数据;
        qfq: 返回前复权后的数据; hfq: 返回后复权后的数据; hfq-factor: 返回后复权因子; hfq-factor: 返回前复
    实例：
    get_sina_kline(symbol='sh000001', period='60m', market='股票')
    get_sina_kline(symbol='sh000001', period='d', market='股票')
    get_sina_kline(symbol='rb1910', period='60m', market='期货')
    get_sina_kline(symbol='rb1910', period='d', market='期货')
    get_sina_kline(symbol='IF1908', period='60m', market='股指期货')
    get_sina_kline(symbol='IF1908', period='d', market='股指期货')
    说明：
    股票历史数据API:
    5分钟：https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sh000001&scale=5&datalen=1023
    15分钟：https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sh000001&scale=15&datalen=1023
    30分钟：https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sh000001&scale=30&datalen=1023
    60分钟：https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sh000001&scale=60&datalen=1023
    商品期货历史数据API:
    5分钟：http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol=rb1910
    15分钟：http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine15m?symbol=rb1910
    30分钟：http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine30m?symbol=rb1910
    60分钟：http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine60m?symbol=rb1910
    日K线：http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=rb1910
    股指期货历史数据API:
    5分钟：http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine5m?symbol=IF1908
    15分钟：http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine15m?symbol=IF1908
    30分钟：http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine30m?symbol=IF1908
    60分钟：http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine60m?symbol=IF1908
    日线：http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesDailyKLine?symbol=IF1908
    '''
    cols = ['date', 'open', 'high', 'low', 'close', 'volume']
    if market == '股票':
        if period in ['5m', '15m', '30m', '60m']:
            url = 'https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=%s&scale=%s&datalen=1023' % (
                symbol, period[:-1])
        else:
            data=lambda key,default:kwargs[key] if key in kwargs else default
            start_date=data('start_date', '19900101')
            end_date = data('end_date', '20000101')
            adjust = data('adjust', '')
            df= ak.stock_zh_a_daily(symbol, start_date, end_date, adjust)
            return df[cols]
 
    elif market=='期货':
        if period in ['5m', '15m', '30m', '60m']:
            url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine%s?symbol=%s' % (
                period, symbol)
        else:
            url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=%s' % (
                symbol)
    else:
        if period in ['5m', '15m', '30m', '60m']:
            url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine%s?symbol=%s' % (
                period, symbol)
        else:
            url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesDailyKLine?symbol=%s' % (
                symbol)
 
    req = request.Request(url)
    rsp = request.urlopen(req)
    res = rsp.read()
    res_json = json.loads(res)
    df= pd.DataFrame(res_json)
    if market == '股票':
        df.rename(columns={'day':'date'}, inplace=True)
        df =df[cols]
    else:
        df.rename(columns=dict(zip(df.columns,cols)), inplace=True)
    return df
 
 
# global_gdp_radio_quarterly()
print(get_sina_kline(symbol='IF1908', period='d', market='股指期货'))