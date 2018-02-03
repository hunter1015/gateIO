import numpy
import pylab
import time
import matplotlib.pyplot as plt
import math

#http://blog.csdn.net/zwq912318834/article/details/78476842?locationNum=4&fps=1
#python用最小二乘法分析数据趋势以及做数据预测



#http://30daydo.com/article/205
#监控聚币网行情 并实时发送到微信


def MA_xielv(madata):
    # 设置横坐标和纵坐标的值
    # def arange(start=None, stop=None, step=None, dtype=None)
    maxValue = max(madata)
    x = numpy.arange(0, len(madata) * madata[0], madata[0])
    print('长度x=',len(x))
    #y = numpy.array([(x-madata[-1]) for x in madata])
    y = numpy.array(madata)
    print('长度y=', len(y))
    z = numpy.polyfit(x, y, 1)
    p = numpy.poly1d(z)
    #plt.plot(p)
    #plt(p)
    #plt.show()

    return p,maxValue



#ma_data = [0.02024,0.02018,0.0201,0.02002,0.01996,0.01992,0.01984,0.01984,0.01984,0.01982,0.01978,0.01984,0.01984,0.01986,0.01988,0.0199,0.0199,0.01992,0.01994,0.01998,0.02004,0.0201,0.02008,0.02006,0.02002,0.01994,0.01988,0.01988,0.0198,0.01972,0.01968,0.01962,0.01958,0.01962,0.01964,0.01964,0.01964,0.0196,0.01958,0.01956,0.01956,0.01958,0.0196,0.01958,0.0196,0.01958,0.01954,0.01952]
#ma_data = [0.02024,0.02018,0.0201,0.02002,0.01996,0.01992,0.01984,0.01984,0.01984,0.01982,0.01978,0.01984,0.01984,0.01986]
#ma_data=[1000,998,996,997,995,996,994,994,993,992]
#ma_data = [0.0168, 0.0168, 0.0168, 0.0169, 0.0169, 0.0169, 0.0169, 0.0169, 0.0169, 0.0169, 0.0169, 0.0169, 0.0169, 0.017, 0.0171, 0.0171, 0.0171, 0.0172, 0.0172, 0.0172]
ma_data = [168, 168, 168, 169, 169, 169, 169, 169, 169, 169, 169, 169, 169, 170, 171, 171, 171, 172, 172, 172]


#ma_data=[10.00,9.98,9.96,9.97,9.95,9.96,9.94,9.94,9.93,9.92]
##-0.007576 x + 9.989 
starttime=time.time()
xielv,zuida=MA_xielv(ma_data)
endtime=time.time()
print(xielv,'   耗时',endtime-starttime)
#print(round(xielv[0],5),'   耗时',endtime-starttime)
#print(round(xielv[0],7),'   耗时',endtime-starttime)
#print(math.sin(math.radians(5)))
#print(math.sin(1,100))



ask=[5,4,3,2,1,3,5,7]
print(ask[:-4:-1])
print(ask[-4:-1])

madata= madata= [0.10516,0.10534,0.1055,
                 ]
x = numpy.arange(0, len(madata) * madata[0], madata[0])
print('x长度=',len(x))
print('x=',x)
