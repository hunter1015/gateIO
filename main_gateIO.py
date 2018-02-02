#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

#pip install matplotlib  安装图形界面  
#【未解决】matplotlib绘图运行不显示问题，修改文件Preferences=>Browse Packages=>Default=>exec.py 大概在39行：
#注释本行   startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW 
#http://python.jobbole.com/87471/ 有个教程 还不错numpy和matplotlib
#


import talib
import numpy as np
import pandas as pd


#K线图
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import datetime as dt
import pylab

#写入csv文件
import random
import csv
import time
from datetime import datetime


import threading


from gateAPI import GateIO

# 填写 APIKEY APISECRET
apikey = '95E7BBF8-51DB-4557-8FF9-4C3542C108DB'
secretkey = '13b1aeb9532ba6e60d93dc036cbe3ad60e7baa14301c85d7a9ee813238a3f564'
API_URL = 'data.gate.io'



klineFilespath = 'C:\\Kline\\'
startdate = dt.date(2017, 8, 29)
enddate = dt.date(2018, 1, 17)
coinCode='btc_usdt'


#指标 MA
MA5 = 5
MA12 = 12
MA26 = 26


MA_5_List=[]
MA_12_List=[]
MA_26_List=[]


MA_1min_5_List=[]
MA_1min_12_List=[]
MA_1min_26_List=[]

MA_5min_5_List=[]
MA_5min_12_List=[]
MA_5min_26_List=[]


MA_15min_5_List=[]
MA_15min_12_List=[]
MA_15min_26_List=[]


MA_30min_5_List=[]
MA_30min_12_List=[]
MA_30min_26_List=[]


orders_usdt=[]

my_account={"result": "true",
            "available": {
            "USDT": "342",
            "GTC": "1799.3293668",
            "DOGE": "31519.06716815",
            "BTM": "499",
            "XRP":"19.964",
            "BCX":"7547.18663707"
            },
            "locked": {
            "USDT": "0",
            "GTC": "0",
            "DOGE": "0",
            "BTM": "0",
            "XRP":"0",
            "BCX":"0"
            }
    }

my_price={"USDT": 0,"GTC": 0,"DOGE": 0,"BTM": 0,"BCX": 0,"XRP": 0}


money_get=0
money_loss=0




createVar = locals()



#print("123"+apikey+"dasd"+secretkey)
gate = GateIO(API_URL,apikey,secretkey)



'''
def read_kData(rootpath,coincode,starttime,endtime):
	returnData=pd.DataFrame()
	for yearnum in range(0,int((endtime - starttime).days / 365.25)+1):
		theyear=starttime+dt.timedelta(days=yearnum*365)
		print('yearnum=',yearnum,'  theyear=',theyear)
		filename=rootpath+theyear.strftime('%Y')+'\\'+str(coincode).zfill(6)+'.csv'
        try:
        	rawdata = pd.read_csv(filename, parse_dates = True, index_col = 0, encoding = 'gbk')
        except IOError:
        	raise Exception('IoError when reading dayline data file: ' + filename)
        returndata = pd.concat([rawdata, returndata])
    #清洗数据    
    returndata = returndata.sort_index()
    returndata.index.name = 'DateTime'
    returndata.drop('amount', axis=1, inplace = True)
    returndata.columns = ['Open', 'High', 'Close', 'Low', 'Volume']
    returndata = returndata[returndata.index < eday.strftime('%Y-%m-%d')]
    return returndata
'''



''' 保存K线到CSV文件中  原版代码
def save2csv(coincode):
	i = 1
	while i > 0:
    i += 1
    url = 'https://www.okcoin.cn/api/v1/trades.do?symbol=eth_cny'
    response = urllib.request.urlopen(url, timeout=3)  # 打开连接，timeout为请求超时时间
    data = response.read().decode('utf-8')  # 返回结果解码
    json_data = json.loads(data)
    print(json_data)
    def main(json_data):
        with open("d:\okcoin.csv", 'w') as f:
            dw = csv.DictWriter(f, json_data[0].keys())
            dw.writeheader()
            for row in json_data:
                dw.writerow(row)
    time.sleep(1)  # 休眠0.1秒
'''




def MA(data,para):
    MAdata =talib.MA(data, para)
    return MAdata


def order_Buy():
    pass


def order_Sell():
    pass


#时间戳变时间
def timeShift(timein):
    time_local = time.localtime(int(timein)/1000)
                #dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
                #利用strptime()函数将时间转换成时间数组
                #利用strftime()函数重新格式化时间
                #
    timeout = time.strftime("%Y-%m-%d :%H:%M:%S",time_local)
                #print(dt)
    timeout = datetime.strptime(timeout,"%Y-%m-%d :%H:%M:%S")
    return timeout

#画K线
def kline_paint(kdata):
    days=kdata
    days = days.sort_index()
    #days.index.name = 'DateTime'
    #days.drop('amount', axis=1, inplace = True)
    #days.columns = ['Open', 'High', 'Close', 'Low', 'Volume']


    daysreshape = days.reset_index()
    #print('daysreshape\n',daysreshape)
    
    # convert the datetime64 column in the dataframe to 'float days'
    # # 对时间数据转换成candlestick_ohlc()方法可读取的格式
    daysreshape['date']=mdates.date2num(daysreshape['date'].astype(dt.date))
    #daysreshape['date']=mdates.date2num(daysreshape['date'])
    #daysreshape['date']=mdates.date2num(daysreshape['date'].astype(dt.date))
    # clean day data for candle view 
    daysreshape.drop('volume', axis=1, inplace = True)
    daysreshape = daysreshape.reindex(columns=['date','open','high','low','close'])  
    #print('daysreshape\n',daysreshape)
    #print(daysreshape.close.values)
    #
    #请注意计算需要内容为float类型的
    Av1 =talib.MA(daysreshape.close.values, MA5)
    Av2 =talib.MA(daysreshape.close.values, MA12)
    #Av1 = movingaverage(daysreshape.close.values, MA1)
    #Av2 = movingaverage(daysreshape.close.values, MA2)
    SP = len(daysreshape.date.values[MA2-1:])
    #print('SP为\n',SP,' 类型为',type(SP))
    print('daysreshape.values[-118:]\n',daysreshape.values[-SP:])

    ##画图自己修改
    fig = plt.figure(facecolor='#07000d',figsize=(15,10))
    ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
    Label1 = str(MA1)+' SMA'
    Label2 = str(MA2)+' SMA'
    ax1.plot(daysreshape.date.values[-SP:],Av1[-SP:],'#e1edf9',label=Label1, linewidth=1.5)
    ax1.plot(daysreshape.date.values[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(20))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d :%H:%M:%S'))
    ax1.yaxis.label.set_color("w")
    ax1.spines['bottom'].set_color("#5998ff")
    ax1.spines['top'].set_color("#5998ff")
    ax1.spines['left'].set_color("#5998ff")
    ax1.spines['right'].set_color("#5998ff")
    ax1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Stock price and Volume')
    plt.show()

    # 创建一个子图 
    '''
    fig, ax = plt.subplots(facecolor=(0.5, 0.5, 0.5))
    fig.subplots_adjust(bottom=0.2)
    # 设置X轴刻度为日期时间
    ax.xaxis_date()
    # X轴刻度文字倾斜45度
    plt.xticks(rotation=45)
    plt.title("股票代码：601558两年K线图")
    plt.xlabel("时间")
    plt.ylabel("股价（元）")
    candlestick_ohlc(ax,daysreshape.values[-SP:],width=.2,colorup='r',colordown='green')
    plt.grid(True)
    plt.show()
    '''
    '''原版备份
    fig = plt.figure(facecolor='#07000d',figsize=(15,10))
    ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
    #其中要求
    candlestick_ohlc(ax1, daysreshape.values[-SP:], width=.6, colorup='#ff1717', colordown='#53c156')
    Label1 = str(MA1)+' SMA'
    Label2 = str(MA2)+' SMA'
    
    ax1.plot(daysreshape.date.values[-SP:],Av1[-SP:],'#e1edf9',label=Label1, linewidth=1.5)
    ax1.plot(daysreshape.date.values[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d :%H:%M:%S'))
    ax1.yaxis.label.set_color("w")
    ax1.spines['bottom'].set_color("#5998ff")
    ax1.spines['top'].set_color("#5998ff")
    ax1.spines['left'].set_color("#5998ff")
    ax1.spines['right'].set_color("#5998ff")
    ax1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Stock price and Volume')
    plt.show()
    '''



    #print(json_data)
def write2file_1min_12hour(coincode):
    firstFlag=0
    i = 1
    kline_data_last=None
    kline_update_point=None
    while i<100:
        i+=1
        kline_data=None
        kline_data = gate.getKline(coincode,'60','12',None)
        #检测本次和上次获取的数据是否一致，如果一致则不操作
        if kline_data==kline_data_last:
            time.sleep(1+random.random())
            #print('检查和上次读取的数据相同，本次不操作')
            continue
        #保存本次数据，作为last数据，勇于下次检查
        kline_data_last=kline_data
        #print(kline_data)
        kline_data_list=[x for x in kline_data.split('\n')[0:-1]]
        if firstFlag==0:
            print(timeShift(kline_data_list[-1].split(',')[0]))
            #kline_data_list_closeData=[x for x in kline_data_list[1:].split(',')[4]]
            #kline_data_list_closeData=[x for x in kline_data.split('\n')[0:-1].split(',')[4]]
            #print(kline_data_list_closeData)
            head=[x for x in kline_data_list[0].split(',')]
            kLineDic = [dict(zip(head, x.split(','))) for x in kline_data_list[1:]]
            #print(kLineDic['close'])
            kline_data_list_closeData=[float(x['close']) for x in kLineDic[0:]]
            #MA(float(kLineDic['close'].values),5)
            #MA(float(kLineDic['close'].values),5)
            #MA(kline_data_list_closeData,12)
            kline_data_list_closeData_np=np.array(kline_data_list_closeData)
            MA_5_List=MA(kline_data_list_closeData_np,5)
            MA_12_List=MA(kline_data_list_closeData_np,12)
            MA_26_List=MA(kline_data_list_closeData_np,26)

            '''
            for x in range(len(MA_5_List)-1,-1,-1):
            #for x,y,z in MA_5_List[0:],MA_12_List[0:],MA_26_List[0:]:
                if MA_5_List[x]>MA_12_List[x] and MA_12_List[x]>MA_26_List[x]
                    print('MA5>MA12>MA26',x)
            '''
            #csv文件写入-MA指标的内容
            MAcsv = pd.DataFrame({'MA 5':MA_5_List,'MA12':MA_12_List,'MA26':MA_26_List})
            #print(MAcsv)
            MAcsv.to_csv("d:\\MA_1MIN.csv",index=False,sep=',')
            ma_data_update=kline_data_list_closeData[-25:]
            print(ma_data_update)


            #print(kline_data_list_closeData)

        #print('kline_data_list[-1]=',kline_data_list[-1],'kline_update_point=',kline_update_point)
        #检查本次更新数据的位置，与已有数据进行对比
        messageWrong=0
        if firstFlag!=0:
            position=0
            for x in kline_data_list[::-1]:
                if x==kline_update_point:
                    #print('x=',x,' kline_update_point=',kline_update_point)
                    #print('position',position)
                    break
                if x.split(',')[0]==kline_update_point.split(',')[0]:
                    #print('发现数据不一致的地方\nx=',x,' kline_update_point=',kline_update_point)
                    break
                if position==0 and x.split(',')[0]<kline_update_point.split(',')[0]:
                    #print('x=',x,' kline_update_point=',kline_update_point)
                    messageWrong=1
                    break
                position+=1
            if(position>20):
                #print('本次数据不包含更新数据，所以跳过')
                continue         
            if messageWrong==1:
                #print('本次数据不包含更新数据，所以跳过')
                continue
            if position==0:
                #print('本次数据不包含更新数据，所以跳过')
                continue
        #else:
         #   kline_update_point=




        '''处理获取的get数据，转化为datafram格式
        klineList = [x for x in kline_data.split('\n')[0:-2]]
        head=[x for x in klineList[0].split(',')]
        kLineDic = [dict(zip(head, x.split(','))) for x in klineList[1:]]
        for x in kLineDic:
            #转换成新的时间格式(2016-05-05 20:28:54)
            #print(x['date'])
            #http://blog.csdn.net/xuezhangjun0121/article/details/78083717
            #13位时间戳转换时间
            time_local = time.localtime(int(x['date'])/1000)
            #dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            #利用strptime()函数将时间转换成时间数组
            #利用strftime()函数重新格式化时间
            #
            dt = time.strftime("%Y-%m-%d :%H:%M:%S",time_local)
            #print(dt)
            dt = datetime.strptime(dt,"%Y-%m-%d :%H:%M:%S")
            #print(dt)
            #dt_array=
            x['date']=dt
            x['open']=float(x['open'])
            x['high']=float(x['high'])
            x['low']=float(x['low'])
            x['close']=float(x['close'])
            x['volume']=float(x['volume'])
            #print(x['date'])                                    
        #转换成localtime
        #print('kLineDic类型为',type(kLineDic))
       # print(kLineDic)
        returndata = pd.DataFrame(kLineDic)
        #returndata=kLineDic
        #returndata = pd.concat([kLineDic, returndata])
        '''



        #画图
        #kline_paint(returndata)

        
        #print('服务器响应的string K线data转换为dic',dList)
        coincode=coincode
        if firstFlag==0:
            with open("d:\\"+coincode+".csv", "w+") as f:
            #dw = csv.DictWriter(f, json_data[0].keys())
            #dw.writeheader()
                f.write(kline_data)
                #klineList = [x for x in kline_data.split('\n')[0:-2]]
                kline_update_point=kline_data_list[-1]
                firstFlag=1
                print("第一次文件初始化，写入完成,kline_update_point=",kline_update_point)
        else:
            with open("d:\\"+coincode+".csv", "a+") as f:
                #dw = csv.DictWriter(f, json_data[0].keys())
                #dw.writeheader()
                #f.write("\n更新位置\n")
                #f.write(kline_data_list[-2-position,-2])
                
                '''
                for x in range(-2-position,-2):
                    #kline_data_list[-2-position,-2]   
                    f.write(kline_data_list[x])
                    print(kline_data_list[x])
                '''
                
                #更新kline数据 更新写入
                for x in range(-2-position+2,0):
                    #kline_data_list[-2-position,-2]
                    ma_data_update.append(float(kline_data_list[x].split(',')[4])) 
                    f.write(kline_data_list[x]+'\n')
                    #print(kline_data_list[x])
                print('更新',position,'条数据,最新数据时间为',timeShift(kline_data_list[-1].split(',')[0]))
                #更新指标-MA的原始数据
                ma_data_update_data_np=np.array(ma_data_update)

                ma5update=MA(ma_data_update_data_np,5)
                ma12update=MA(ma_data_update_data_np,12)
                ma26update=MA(ma_data_update_data_np,26)

                with open('d:\\MA_1MIN.csv','a+',newline='') as f:
                    writer = csv.writer(f)
                    for row in range(25,len(ma5update)):
                        #row.append(row[len(row)-1])
                        #print(ma5update[row],',',ma12update[row],',',ma26update[row])
                        writer.writerow([ma5update[row],ma12update[row],ma26update[row]])
                        #writer.writerow(ma5update[row]+','+ma12update[row]+','+ma26update[row])
                #f.write(kline_data_list[x]+'\n')

                #保存MA值的三张列表，把更新的MA值加进去，更新的几条K线数据通过向前倒退25个数据，来完成5\12\26的计算，再
                #从这几条新数据截取一下，放回原来的数组中
                MA_5_List=np.append(MA_5_List,ma5update[25:])
                MA_12_List=np.append(MA_12_List,ma12update[25:])
                MA_26_List=np.append(MA_26_List,ma26update[25:])
                #print('MA_5_List 长度为',len(MA_5_List),' 值为\n',MA_5_List)

                

                kline_update_point=kline_data_list[-1]

                print("文件更新，写入完成,kline_update_point=",kline_update_point)
                '''
                dw = file.writer(f)
                for row in kline_data.split('\n'):
                    dw.writerow(row)
                '''
        print('本次请求结束,休眠\n')
          # 休眠0.1秒
        time.sleep(1+random.random())
    return "write2file结束"


#print(write2file_1min_12hour('btc_usdt'))



def write2file_5min_24hour(coincode,if_is_first,datalast,ma5,ma12,ma26):
    #判断是否为第一次执行（建立文件，全部更新）
    firstFlag=if_is_first
    kline_data_last=datalast
    kline_update_point=None
    kline_data=None
    kline_data = gate.getKline(coincode+'_usdt','300','24',None)
    #检测本次和上次获取的数据是否一致，如果一致则不操作
    if kline_data==datalast:
        #time.sleep(1+random.random())
        #print('检查和上次读取的数据相同，本次不操作')
        return datalast,ma5,ma12,ma26

    

    #保存本次数据，作为last数据，勇于下次检查
    #datalast=kline_data
    #print(kline_data)
    kline_data_list=[x for x in kline_data.split('\n')[0:-1]]
    #print("kline_data_list[-1]=",kline_data_list[-1])
    #方法参数的 第一次参数如果设置为0  说明为第一次
    if firstFlag==0:
        #print('时间偏差:当前时间为',timeShift(time.time()),'  最新信息时间为',timeShift(kline_data_list[-1].split(',')[0]))
        head=[x for x in kline_data_list[0].split(',')]
        kLineDic = [dict(zip(head, x.split(','))) for x in kline_data_list[1:]]
        kline_data_list_closeData=[float(x['close']) for x in kLineDic[0:]]

        kline_data_list_closeData_np=np.array(kline_data_list_closeData)
        ma5=MA(kline_data_list_closeData_np,5)
        ma12=MA(kline_data_list_closeData_np,12)
        ma26=MA(kline_data_list_closeData_np,26)

        ''' 将MA值保存到文件中
        MAcsv = pd.DataFrame({'MA 5':ma5,'MA12':ma12,'MA26':ma26})
        #print(MAcsv)
        MAcsv.to_csv('d:\\'+coincode+'_MA_5min_24h.csv',index=False,sep=',')
        #旧版本 用于保存最后一个向前推25个值的list  勇于计算MA26
        #ma_data_update=kline_data_list_closeData[-25:]
        '''


    #检查本次更新数据的位置，与已有数据进行对比
    messageWrong=0
    if firstFlag!=0:
        data_Last_finalValue=datalast[-1]
        #print('data_Last_finalValue=',data_Last_finalValue)
        position=0
        for x in kline_data_list[::-1]:
            if x==data_Last_finalValue:
                break
            if x.split(',')[0]==data_Last_finalValue.split(',')[0]:
                #print('发现数据不一致的地方\nx=',x,' kline_update_point=',kline_update_point)
                break
            if position==0 and x.split(',')[0]<data_Last_finalValue.split(',')[0]:
                #print('x=',x,' kline_update_point=',kline_update_point)
                messageWrong=1
                break
            position+=1
        #print('position=',position)
        if(position>10):
            #print('本次数据不包含更新数据，所以跳过')
            return datalast,ma5,ma12,ma26         
        if messageWrong==1:
            #print('本次数据不包含更新数据，所以跳过')
            return datalast,ma5,ma12,ma26
        if position==0:
            #print('本次数据不包含更新数据，所以跳过')
            return datalast,ma5,ma12,ma26
    #else:
     #   kline_update_point=

    
    #print('服务器响应的string K线data转换为dic',dList)
    coincode=coincode
    if firstFlag==0:
        '''
        with open("d:\\"+coincode+"_5min_24h.csv", "w+") as f:
        #dw = csv.DictWriter(f, json_data[0].keys())
        #dw.writeheader()
            f.write(kline_data)
            #klineList = [x for x in kline_data.split('\n')[0:-2]]
            #kline_update_point=kline_data_list[-1]
            #print("第一次文件初始化，写入完成,kline_update_point=",kline_update_point)
        '''
    else:
        #print("数据更新")
        '''  更新文件 带文件的版本
        with open("d:\\"+coincode+"_5min_24h.csv", "a+") as f:              
            #更新kline数据 更新写入
            #ma_data_update=[float(x['close']) for x in kLineDic[0:]]
            ma_data_update=[float(x.split(',')[4]) for x in kline_data_list[-25:]]
            for x in range(-2-position+2,0):
                #kline_data_list[-2-position,-2]
                ma_data_update.append(float(kline_data_list[x].split(',')[4])) 
                f.write(kline_data_list[x]+'\n')
                #print(kline_data_list[x])
            #print('更新',position,'条数据,最新数据时间为',timeShift(kline_data_list[-1].split(',')[0]))
            #更新指标-MA的原始数据
            ma_data_update_data_np=np.array(ma_data_update)

            ma5update=MA(ma_data_update_data_np,5)
            ma12update=MA(ma_data_update_data_np,12)
            ma26update=MA(ma_data_update_data_np,26)

            with open('d:\\'+coincode+'_MA_5min_24h.csv','a+',newline='') as f:
                writer = csv.writer(f)
                for row in range(25,len(ma5update)):
                    #row.append(row[len(row)-1])
                    #print(ma5update[row],',',ma12update[row],',',ma26update[row])
                    writer.writerow([ma5update[row],ma12update[row],ma26update[row]])
                    #writer.writerow(ma5update[row]+','+ma12update[row]+','+ma26update[row])
            #f.write(kline_data_list[x]+'\n')
            '''

        #不更新文件 带文件的版本
    #with open("d:\\"+coincode+"_5min_24h.csv", "a+") as f:
        #更新kline数据 更新写入
        #ma_data_update=[float(x['close']) for x in kLineDic[0:]]
        ma_data_update=[float(x.split(',')[4]) for x in kline_data_list[-25:]]
        for x in range(-2-position+2,0):
            #kline_data_list[-2-position,-2]
            ma_data_update.append(float(kline_data_list[x].split(',')[4]))
            #f.write(kline_data_list[x]+'\n')
            #print(kline_data_list[x])
        #print('更新',position,'条数据,最新数据时间为',timeShift(kline_data_list[-1].split(',')[0]))
        #更新指标-MA的原始数据
        ma_data_update_data_np=np.array(ma_data_update)
        ma5update=MA(ma_data_update_data_np,5)
        ma12update=MA(ma_data_update_data_np,12)
        ma26update=MA(ma_data_update_data_np,26)

        ma5=np.append(ma5,ma5update[25:])
        ma12=np.append(ma5,ma12update[25:])
        ma26=np.append(ma5,ma26update[25:])

    return kline_data_list,ma5,ma12,ma26



def update_orderBooks(coincode):
    #global orders_btc_usdt
    responseData=gate.orderBook(coincode)
    
    if(responseData=='no data' or responseData=='timeout'):
        #print("异常处理")
        #time.sleep(0.6+random.random())
        return "异常"
    return responseData
    #print('更新完成\n',orders_btc_usdt['bids'][0])


'''
            "GTC": "499",
            "DOGE": "11978",
            "BTM": "499",
'''

#def sell_10up():

#def sell_4up():

def xielv(madata):
    # 设置横坐标和纵坐标的值
    # def arange(start=None, stop=None, step=None, dtype=None)
    maxValue = max(madata)
    minValue =  min(madata)
    x = np.arange(1, len(madata) + 1, 1)
    y = np.array(madata)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    return round(z[0],4),maxValue,minValue


def sell(price,volume,orders,coin_name):
    moneySell=0
    money_chengben=0
    money_profit=0
    money_my=my_price[coin_name.upper()]

    for x in orders[0:3]:
        if(volume==0):
            break
        bid_price=float(x[0])
        bid_volum=float(x[1])
        if bid_price>price:
            if bid_volum>volume:
                money_sell=money_sell+bid_price*volume*0.998
                money_chengben=money_chengben+money_my*volume
                #money_profit=money_profit+money_sell-money_chengben
                volume=0
                break
            if bid_volum<volume:
                money_sell=money_sell+bid_price*bid_volum*0.998
                money_chengben=money_chengben+money_my*bid_volum
                #money_profit=money_profit+money_sell-money_chengben
                volume=volume-bid_volum
                continue
    return volume,money_sell,money_sell-money_chengben

 
def sell_run(volume,orders,coin_name):
    moneySell=0
    money_chengben=0
    money_profit=0
    money_my=my_price[coin_name.upper()]
    for x in orders[0:3]:
        if(volume==0):
            break
        bid_price=float(x[0])
        bid_volum=float(x[1])
        if bid_volum>volume:
                money_sell=money_sell+bid_price*volume*0.998
                money_chengben=money_chengben+money_my*volume
                #money_profit=money_profit+money_sell-money_chengben
                volume=0
                break
        if bid_volum<volume:
                money_sell=money_sell+bid_price*bid_volum*0.998
                money_chengben=money_chengben+money_my*bid_volum
                #money_profit=money_profit+money_sell-money_chengben
                volume=volume-bid_volum
                continue
    return volume,money_sell,money_sell-money_chengben

def buy(price,money_left,orders,coin_name):
    money_buy=0
    volum_incress=0
    temp_volum=0
    money_left=0

    for x in orders[:-4:-1]:
        if(money_left<0.5):
            break
        ask_price=float(x[0])
        ask_volum=float(x[1])
        if ask_price<price:
            temp_volum=money_left*0.995/ask_price
            if ask_volum>temp_volum:
                volum_incress=volum_incress+temp_volum
                money_left=0
                break
            if ask_volum<temp_volum:
                volum_incress=volum_incress+ask_volum
                money_left=money_left-ask_volum*ask_price*1.005
                continue
    return volum_incress,money_left


#USDT余额 锁
lock = threading.Lock()

def action_go(coin_name):
    print(coin_name,"监控开始")

    #更新K线文件信息（1分、5分、15分、30分）
    #kdata_update_1min_12hour = threading.Thread(target=write2file_1min_12hour('btc_usdt'))
    #kdata_update_1min_12hour.start()
    #kdata_update_1min_12hour.join()

    #order_update = threading.Thread(target=update_orderBooks('btc_usdt'))
    #order_update.start()
    money_get=0
    money_loss=0
    loopFlag=0
    loopNumber=0
    dealNumber=0
    datalast=None
    ma_5=None
    ma_12=None
    ma_26=None
    ma5_xielv=0
    ma12_xielv=0
    ma5_xielv_last=0
    ma12_xielv_last=0


    ma_5_max=0
    ma_12_max=0
    ma_5_min=0
    ma_12_min=0
    '''
        createVar coin_name_+'MA_5min_5_List' as t1
        createVar coin_name_+'MA_5min_12_List' as
        createVar coin_name_+'MA_5min_26_List'
    '''
    tp1,tp2,tp3,tp4=write2file_5min_24hour(coin_name,0,datalast,ma_5,ma_12,ma_26)
    datalast=tp1
    ma_5=tp2
    ma_12=tp3
    ma_26=tp4
    ma5_xielv, ma_5_max = xielv(ma_5[-3:])
    ma12_xielv, ma_12_max = xielv(ma_12[-3:])

    #datalast,ma_5,ma_12,ma_26=write2file_5min_24hour(coin_name,0,datalast,ma_5,ma_12,ma_26)
    
    orders=update_orderBooks(coin_name+'_usdt')
    #update_orderBooks('btm_usdt')
    my_price[coin_name.upper()]=0
    chengbenPrice=0
    for x in orders['bids'][0:3]:
        chengbenPrice=chengbenPrice+float(x[0])
    my_price[coin_name.upper()]=(chengbenPrice/3)*0.7
    #print(coin_name,'成本价初始化为',my_price[coin_name.upper()])
    #float(orders_btc_usdt['bids'][0:3][0])#+orders_btc_usdt['bids'][-3][0]+orders_btc_usdt['bids'][-3][0])
    orders_last=orders

    #订单簿存储
    '''
    bid_price=[]
    bid_volum=[]

    ask_price=[]
    ask_volum=[]

    for x in orders['bids'][0:5]:
            bid_price.append(x[0])
            bid_volum.append(x[1])

    for x in orders['asks'][::-5]:
            ask_price.append(x[0])
            ask_volum.append(x[1])
    '''

    tradeHistorys_sell_price=[]
    tradeHistorys_sell_volum=[]

    tradeHistorys_buy_price=[]
    tradeHistorys_buy_volum=[]


    tradeHistorys=[]
    tradeHistorys_last=[]





    while True:
        #temp=write2file_5min_24hour(coin_name,1,datalast)


        #更新账户信息
        #print(gate.balances())

        data_new=0

        temp,ma1,ma2,ma3=write2file_5min_24hour(coin_name,1,datalast,ma_5,ma_12,ma_26)


        #更新交易簿 orders
        #print("datalast.split('\n')[-2]=",datalast.split('\n')[-2])
        
        orders=update_orderBooks(coin_name+'_usdt')

        if datalast!=temp:
            data_new=1
            datalast=temp
            ma_5=ma1
            ma_12=ma2
            ma_26=ma3


        loopFlag=loopFlag+1
        if(loopNumber==0):
            startTime=time.time()
        if(loopNumber==1):
            endTime=time.time()
            print("本线程一次时间消耗为",endTime-startTime)
        loopNumber=loopNumber+1
        #if loopFlag>20:
            
        if loopFlag>100:
            loopFlag=0
            #print('买1=',orders_btc_usdt['bids'][0],' 上次买1=',orders_btc_usdt_last['bids'][0],' 当前库存=',float(my_account['available'][coin_name.upper()]))
            #print(coin_name,'请求',loopNumber,'次,','成交',dealNumber,'次,当前库存=',float(my_account['available'][coin_name.upper()]))
            #print(coin_name,'当前买1=',orders['bids'][0],' 上次买1=',orders_last['bids'][0])
        if(orders=='异常'):
            #print(coin_name,"异常处理")
            time.sleep(0.6+random.random())
            continue
        #print('买1=',orders_btc_usdt['bids'][0],' 上次买1=',orders_btc_usdt_last['bids'][0],' 当前库存=',float(my_account['available'][coin_name.upper()]))
        if(orders_last==orders):
            #print("本次和上次数据相同")
            #time.sleep(0.6+random.random())
            continue
        orders_last=orders
        #print(orders_btc_usdt['asks'][-1][0])
        '''卖方
        ask1=orders_btc_usdt['asks'][-1][0]
        ask1_volum=orders_btc_usdt['asks'][-1][1]
        ask2=orders_btc_usdt['asks'][-2][0]
        ask2_volum=orders_btc_usdt['asks'][-2][1]
        ask3=orders_btc_usdt['asks'][-3][0]
        ask3_volum=orders_btc_usdt['asks'][-3][1]
        '''



        ############## 库存与余额检查  确保现金与持仓占比在30%-70%   [暂不考虑]



        ######   卖策略——涨幅到达/拐点及时抛/连续下跌行情抛/

        #print(orders['bids'][0][0])
        '''
        bid_price[0]=orders['bids'][0][0]
        bid_price[1]=orders['bids'][1][0]
        bid_price[2]=orders['bids'][2][0]
        bid_price[3]=orders['bids'][3][0]
        bid_price[4]=orders['bids'][4][0]

        bid_volum[0]=orders['bids'][0][1]
        bid_volum[1]=orders['bids'][1][1]
        bid_volum[2]=orders['bids'][2][1]
        bid_volum[3]=orders['bids'][3][1]
        bid_volum[4]=orders['bids'][4][1]


        ask_price[0]=orders['asks'][-1][0]
        ask_price[1]=orders['asks'][-2][0]
        ask_price[2]=orders['asks'][-3][0]
        ask_price[3]=orders['asks'][-4][0]
        ask_price[4]=orders['asks'][-5][0]

        ask_price[0]=orders['asks'][-1][0]
        ask_price[1]=orders['asks'][-2][0]
        ask_price[2]=orders['asks'][-3][0]
        ask_price[3]=orders['asks'][-4][0]
        ask_price[4]=orders['asks'][-5][0]
        '''

        '''
        for x in orders['bids'][0:5]:
            bid_price.append(x[0])
            bid_volum.append(x[1])

        for x in orders['asks'][::-5]:
            ask_price.append(x[0])
            ask_volum.append(x[1])
        print(ask_price)
       ''' 
        bid1=float(orders['bids'][0][0])
        bid1_volum=float(orders['bids'][0][1])



        ##############   第一操作-大涨卖-检查收益是否瞬间大于10% 那就直接卖掉    收益>10%的情况
        volume_now=float(my_account['available'][coin_name.upper()])
        money_profit=0
        if volume_now*bid1>0.5:
            #如果有库存并且涨幅到了
            if bid1>=my_price[coin_name.upper()]*1.10:
                volume_now,money_sell,money_profit=sell(my_price[coin_name.upper()]*1.10,volume_now,orders['bids'],coin_name)
                my_account['available'][coin_name.upper()]=str(volume_now)
                lock.acquire()
                try:
                    my_account['available']['USDT']=str(float(my_account['available']['USDT'])+money_sell)
                finally:
                    lock.release()

                print(coin_name,"——【大涨卖】涨了超过10%  赶紧卖,获利",money_profit,' 库存为',volume_now,' USDT余额=',my_account['available']['USDT'])
                time.sleep(10)
                continue

        ############## 第二操作-计算技术指标  成交记录斜率/MA斜率/成交量对比 
        #成交历史计算
        tradeHistorys=gate.tradeHistory(coin_name+'_usdt')
        if  tradeHistorys_last!=tradeHistorys  and tradeHistorys!='no data' and tradeHistorys!='timeout' :
            tradeHistorys_last=tradeHistorys
            #print(tradeHistorys['data'][0]['type'])
            tradeHistorys_sell_volum_sum=0
            tradeHistorys_buy_volum_sum=0

            tradeHistorys_sell_price=[]
            tradeHistorys_sell_volum=[]
            tradeHistorys_buy_price=[]
            tradeHistorys_buy_volum=[]


            for x in tradeHistorys['data']:
                rate=float(x['rate'])
                amount=float(x['amount'])

                if x['type']=='sell':
                    tradeHistorys_sell_price.append(rate)
                    tradeHistorys_sell_volum.append(amount)
                    tradeHistorys_sell_volum_sum=tradeHistorys_sell_volum_sum+amount
                if x['type']=='buy':
                    tradeHistorys_buy_price.append(rate)
                    tradeHistorys_buy_volum.append(amount)
                    tradeHistorys_buy_volum_sum=tradeHistorys_buy_volum_sum+amount
            #print(tradeHistorys_buy_price)
            tradeHistorys_sell_price_xielv,tradeHistorys_sell_price_max=xielv(tradeHistorys_sell_price)
            tradeHistorys_buy_price_xielv,tradeHistorys_buy_price_max=xielv(tradeHistorys_buy_price)
        #print('历史价格斜率为,',tradeHistorys_sell_price_xielv,tradeHistorys_sell_price_max)
        #tradeHistorys_sell_price=#['rate']
        #print(tradeHistorys_sell_price)


        #MA指标计算-检测MA异动，检测是否会暴跌套住，准备结合目前成本情况止损  准备抛卖，MA下降的情况
        #计算MA最新3个数值的斜率 如果本次信息和上次相比有更新 才会算MA值
        #data_new=1 意思是检测到本次更新数据与上次不同
        if data_new==1:
            ma5_xielv_last=ma5_xielv
            ma12_xielv_last=ma12_xielv
            ma5_xielv, ma_5_max,ma_5_min = xielv(ma_5[-3:])
            ma12_xielv, ma_12_max ,ma_12_min= xielv(ma_12[-3:])
        #ma26_xielv, ma_26_max = xielv(ma_26[-5:])

        #MA5=MA10  判断两条线的趋势
        #if ma_5[-1]==ma_12[-1]:
         #   if ma5_xielv <0 and tradeHistorys_sell_price_xielv<0 and  ma_5[-1]<ma_5[-2] and ma_5[-1]>ma_12[-1]:




        ##############第三操作   收益大于3% 小于8%的情况   在参考K线情况决定是否卖出
        if volume_now*bid1>0.5:
            #如果有库存并且涨幅到了
            if bid1>=my_price[coin_name.upper()]*1.03:
                #如果成交历史中 卖斜率<0  买斜率<0   /    MA5[-1]<MA5[-2]    /
                if tradeHistorys_sell_price_xielv<0  and tradeHistorys_buy_price_xielv<0 and  ma_5[-1]<ma_5[-2] and ma_5[-1]>ma_12[-1] and ma12_xielv>0:
                    volume_now,money_sell,money_profit=sell(my_price[coin_name.upper()]*1.03,volume_now,orders['bids'],coin_name)
                    my_account['available'][coin_name.upper()]=str(volume_now)

                    lock.acquire()
                    try:
                        my_account['available']['USDT']=str(float(my_account['available']['USDT'])+money_sell)
                    finally:
                        lock.release()

                    print(coin_name,"——【小涨卖】指标不好-涨了超过3% 赶紧卖,  获利",money_profit,' 库存为',volume_now,' USDT余额=',my_account['available']['USDT'])
                    time.sleep(15)
                    continue
        ##############第四操作   行情不好，持续下跌，准备割肉跑路

        #连续两天下跌信号
        double_down=0
        tradeHistorys_sell_duo=0
        #print("datalast[-1]为",datalast[-1])

        data_last_1_closePrice=datalast[-1].split(',')[4]
        data_last_1_openPrice=datalast[-1].split(',')[1]

        data_last_2_closePrice=datalast[-2].split(',')[4]
        data_last_2_openPrice=datalast[-2].split(',')[1]


        if data_last_1_openPrice>data_last_1_closePrice and data_last_2_openPrice>data_last_2_closePrice:
            double_down=1
        if tradeHistorys_sell_volum>tradeHistorys_buy_volum:
            tradeHistorys_sell_duo=1

        #如果从高点下降
        if ma_5[-1]>ma_12[-1] and ma_5[-1]<ma[-2] and ma5_xielv<ma5_xielv_last and double_down==1 and tradeHistorys_sell_duo==1 and data_last_1_openPrice>(ma_5_max+ma_5_min)*1.025: #and bid1 my_price[coin_name.upper()]*:
            volume_sell_run_left,money_sell,money_profit=sell_run(volume_now*0.8,orders['bids'],coin_name)
            volume_now=volume_now*0.2+volume_sell_run_left
            my_account['available'][coin_name.upper()]=str(volume_now)
            lock.acquire()
            try:
                my_account['available']['USDT']=str(float(my_account['available']['USDT'])+money_sell)
            finally:
                lock.release()
            print(coin_name,"——【高点跑】 损失",money_profit,' 库存为',volume_now,' USDT余额=',my_account['available']['USDT'])
                   



        if ma_5[-1]==ma_12[-1] and ma_5[-1]<ma_5[-2] and ma5_xielv<ma12_xielv <0 and ma_5[-1]>ma_12[-1] and tradeHistorys_sell_price_xielv<0 and double_down=1:

        #and :

        #print("行情变差 赶紧跑路")
        


        ###############存货无    买操作  
        ##############第一操作   MA5 上穿 MA12
        if volume_now*bid1<100 and float(my_account['available']['USDT']>1:
            if ma_5[-1]==ma_12[-1] and ma_5[-2]<ma_12[-2] and ma5_xielv>0 and ma5_xielv>ma12_xielv:
                    ask1=float(orders['asks'][-1][0])
                    ask1_volum=float(orders['asks'][-1][1])
                    money_to_buy=float(my_account['available']['USDT'])*1/3
                    volume_now,money_left=buy(ask1,money_to_buy,orders['asks'],coin_name)
                    money_cost=money_to_buy-money_left
                    my_account['available'][coin_name.upper()]=str(float(my_account['available'][coin_name.upper()])+volume_now)
                    volume_now=float(my_account['available'][coin_name.upper()])
                    lock.acquire()
                    try:
                        my_account['available']['USDT']=str(float(my_account['available']['USDT'])*2/3+money_left)
                    finally:
                        lock.release()
                    print(coin_name,"——【上穿买】MA指标上穿-买,  花费",money_cost,'  目前库存为',volume_now,' USDT余额=',my_account['available']['USDT'])
            if ma_5[-1]>ma_12[-1] and ma_5[-2]>ma_12[-2] and ma5_xielv>0 and ma12_xielv>0 and ma5_xielv>ma12_xielv and tradeHistorys_buy_price_xielv>0:
                    ask1=float(orders['asks'][-1][0])
                    ask1_volum=float(orders['asks'][-1][1])
                    money_to_buy=float(my_account['available']['USDT'])*1/3
                    volume_now,money_left=buy(ask1,money_to_buy,orders['asks'],coin_name)
                    money_cost=money_to_buy-money_left
                    my_account['available'][coin_name.upper()]=str(float(my_account['available'][coin_name.upper()])+volume_now)
                    volume_now=float(my_account['available'][coin_name.upper()])
                    lock.acquire()
                    try:
                        my_account['available']['USDT']=str(float(my_account['available']['USDT'])*2/3+money_left)
                    finally:
                        lock.release()
                    print(coin_name,"——【上涨趋势买】MA指标上穿-买,  花费",money_cost,'  目前库存为',volume_now,' USDT余额=',my_account['available']['USDT'])


        


        time.sleep(0.1+random.random())
        #print("本次无机会")



    
    print('多线程测试')


    #拿到最新订单簿
    #print (gate.orderBook('btc_usdt'))

    #计算MA5 MA12 MA26的指标并保存
    

    #如果当前 卖1价>持有价*1.2 and  卖1量的检查 与卖2价的检查
    '''
    priceMe=None
    price_Sell_1=None
    if priceMe>price_Sell_1*1.2:
       #order_Sell()
            pass    
    pass
    '''

def printTest(coin_name):
    i=0
    while i<5:
        print(coin_name,threading.current_thread().name)
        i=i+1
        time.sleep(2)


def main():

    '''
    threads = []
    test1 = threading.Thread(target=printTest, args=('btm',),name='btmThread') 
    threads.append(test1)
    test2 = threading.Thread(target=printTest,  args=('bcx',),name='bcxThread')
    threads.append(test2)
    test3 = threading.Thread(target=printTest,  args=('gtc',),name='gtcThread')
    threads.append(test3)




    # 启动所有线程
    for t in threads:
        t.start()
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join() 

    '''
    
    #启动多线程轮训
    btm_thread = threading.Thread(target=action_go, args=('btm',), name='btmThread')
    bcx_thread = threading.Thread(target=action_go, args=('bcx',), name='bcxThread')
    gtc_thread = threading.Thread(target=action_go, args=('gtc',), name='gtcThread')
    btm_thread.start()
    #bcx_thread = threading.Thread(target=action_go('bcx'), name='bcxThread')
    bcx_thread.start()
    gtc_thread.start()

    btm_thread.join()
    bcx_thread.join()

    #gtc_thread = threading.Thread(target=action_go('gtc'), name='gtcThread')
    
    gtc_thread.join()
    
main()
#action_go()
#testlist=gate.getKline('btc_usdt',None,None,None)
'''
testlist=gate.getKline('btc_usdt','60','12',None)
print('testlist类型为',type(testlist),'内容为\n',testlist)

i=0
for x in testlist[::-2]:
    if i>3:
        break;
    print(x)
    i+=1
'''



#plt.plot([1,1,1,1])  
#plt.show() 


# 所有交易对
#print (gate.pairs())




#pairs={}
#pairs=gate.pairs()
#print ("交易货币对为",pairs.get('gtc_usdt'))

#交易对 gtc_usdt

#print (gate.pairs('btc_usdt'))

# 市场订单参数
#print (gate.marketinfo())

#print (gate.marketinfo()['pairs']['gtc_usdt']['fee'])

gtc_market_info_firstCatch=0


#获取gtc手续费
if gtc_market_info_firstCatch==0:
	for i in gate.marketinfo()['pairs']:
		if i.get("gtc_usdt")!=None:
		#print (i['gtc_usdt']["fee"])
			gtc_trade_Fee=i['gtc_usdt']['fee']
			gtc_min_trade_amount=i['gtc_usdt']['min_amount']
			print ('gtc手续费为',gtc_trade_Fee)
			print ('最小交易量为',gtc_min_trade_amount)
			gtc_market_info_firstCatch=1
			break




# 交易市场详细行情
# print (gate.marketlist())


# 所有交易行情
# print (gate.tickers())


# 单项交易行情
# print (gate.ticker('btc_usdt'))
'''
while True:
	gate.ticker('gtc_usdt')
	pass
'''
#print(gate.ticker('gtc_usdt'))




# 所有交易对的市场深度
#print (gate.orderBooks())


# 单项交易对的市场深度
#print (gate.orderBook('btc_usdt'))
#


# 单项交易历史
#print ('单项交易历史 前100条',gate.tradeHistory('btc_usdt'))
#print (gate.tradeHistory('gtc_usdt/3375762'))


#按日志号往前拿出1000条成交历史
#
#
tradeHistoryPriceRecord=[]
'''
for i in gate.tradeHistory('gtc_usdt/3375762')['data']:
	x=i['rate']
	tradeHistoryPriceRecord.append(x)

#print(tradeHistoryPriceRecord)
'''



#测试talib的图形展示，以SMA为例
#SMA=talib.SMA(np.array(tradeHistoryPriceRecord),timeperiod=30)
#print (SMA)




#k线
#
#gate.getKline('btc_usdt',None,None,None)

#print(gate.getKline('btc_usdt',None,None,None))



#画图测试，加入历史交易图和SMA图
#plt.plot(tradeHistoryPriceRecord) 
#plt.plot(SMA) 
#plt.show()
# 获取账号资金
# print (gate.balances())

# 获取充值地址
# print (gate.depositAddres('btc'))

# 获取充值提现历史记录
# print (gate.depositsWithdrawals('1469092370','1569092370'))


# 下单交易买入
# print (gate.buy('etc_btc','0.001','123'))

# 下单交易买入
# print (gate.sell('etc_btc','0.001','123'))


# 取消下单
# print (gate.cancelOrder('267040896','etc_btc'))

# 取消所有订单
# print (gate.cancelAllOrders('0','etc_btc'))


# 获取下单状态
# print (gate.getOrder('267040896','eth_btc'))


# 获取下单状态
# print (gate.openOrders())

# 获取我的24小时内成交记录
# print (gate.mytradeHistory('etc_btc','267040896'))


# 提现
# print (gate.withdraw('btc','88','your address'))
