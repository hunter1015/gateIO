#!/usr/bin/python
# -*- coding: utf-8 -*-

from HttpUtil import getSign,httpGet,httpPost,httpGetKline

class GateIO:

    def __init__(self,url,apikey,secretkey):
        self.__url = url
        self.__apikey = apikey
        self.__secretkey = secretkey

    #所有交易对
    
    def pairs(self):
        URL = "/api2/1/pairs"
        params=''
        return httpGet(self.__url,URL,params)


    #市场订单参数
    def marketinfo(self):
        URL = "/api2/1/marketinfo"
        params=''
        return httpGet(self.__url,URL,params)

    #交易市场详细行情
    def marketlist(self):
        URL = "/api2/1/marketlist"
        params=''
        return httpGet(self.__url,URL,params)
    #所有交易行情
    def tickers(self):
        URL = "/api2/1/tickers"
        params=''
        return httpGet(self.__url,URL,params)

    #单项交易行情
    def ticker(self,param):
        URL = "/api2/1/ticker"
        return httpGet(self.__url,URL,param)


    # 所有交易对市场深度
    def orderBooks(self):
        URL = "/api2/1/orderBooks"
        param=''
        return httpGet(self.__url, URL, param)


    # 单项交易对市场深度
    def orderBook(self,param):
        URL = "/api2/1/orderBook"
        return httpGet(self.__url, URL, param)


    # 历史成交记录
    def tradeHistory(self, param):
        URL = "/api2/1/tradeHistory"
        return httpGet(self.__url, URL, param)




    #获取K线数据 yyh增加
    #币种+间隔(秒)+时间长度 都要是字符串类型的
    #eth_usdt，60,24
    def getKline(self,pairs,timeperiod,timetotal,param):
        param=''
        if pairs==None:
            pairs='eth_usdt'
        if timeperiod==None:
            timeperiod='900'
        if timetotal==None:
            timetotal='24'
        #URL = "https://gate.io/json_svr/query/?u=10&c=380225&type=kline&symbol=eth_usdt&group_sec=900&range_hour=24"
        #URL = "https://gate.io/json_svr/query/?u=10&c=380225&type=kline&symbol="+pairs+"&group_sec="+timeperiod+"&range_hour=24"
        URL = "/json_svr/query/?u=10&c=380225&type=kline&symbol="+pairs+"&group_sec="+str(timeperiod)+"&range_hour="+str(timetotal)
        #print('self.__url='+self.__url)
        return httpGetKline('gate.io',URL,param)




    #获取帐号资金余额
    def balances(self):
        URL = "/api2/1/private/balances"
        param = {}
        return httpPost(self.__url,URL,param,self.__apikey,self.__secretkey)


    # 获取充值地址
    def depositAddres(self,param):
        URL = "/api2/1/private/depositAddress"
        params = {'currency':param}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)


    # 获取充值提现历史
    def depositsWithdrawals(self, start,end):
        URL = "/api2/1/private/depositsWithdrawals"
        params = {'start': start,'end':end}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)


    # 买入
    def buy(self, currencyPair,rate, amount):
        URL = "/api2/1/private/buy"
        params = {'currencyPair': currencyPair,'rate':rate,'amount':amount}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 卖出
    def sell(self, currencyPair, rate, amount):
        URL = "/api2/1/private/sell"
        params = {'currencyPair': currencyPair, 'rate': rate, 'amount': amount}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 取消订单
    def cancelOrder(self, orderNumber, currencyPair):
        URL = "/api2/1/private/cancelOrder"
        params = {'orderNumber': orderNumber, 'currencyPair': currencyPair}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)


    # 取消所有订单
    def cancelAllOrders(self, type, currencyPair):
        URL = "/api2/1/private/cancelAllOrders"
        params = {'type': type, 'currencyPair': currencyPair}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)


    # 获取下单状态
    def getOrder(self, orderNumber, currencyPair):
        URL = "/api2/1/private/getOrder"
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)


    # 获取我的当前挂单列表
    def openOrders(self):
        URL = "/api2/1/private/openOrders"
        params = {}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)


    # 获取我的24小时内成交记录
    def mytradeHistory(self,currencyPair,orderNumber):
        URL = "/api2/1/private/tradeHistory"
        params = {'currencyPair': currencyPair, 'orderNumber': orderNumber}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)

    # 提现
    def withdraw(self,currency,amount,address):
        URL = "/api2/1/private/withdraw"
        params = {'currency': currency, 'amount': amount,'address':address}
        return httpPost(self.__url, URL, params, self.__apikey, self.__secretkey)



