#!/usr/bin/python
# -*- coding: utf-8 -*-

import http.client
import urllib
import json
from hashlib import sha512
import hmac
import requests
import socket

def getSign(params,secretKey):
    sign = ''
    for key in (params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    sign = sign[:-1]
    my_sign = hmac.new( bytes(secretKey,encoding='utf8'),bytes(sign,encoding='utf8'), sha512).hexdigest()
    return my_sign


def httpGet(url,resource,params=''):
    #print('url='+url+'  resource='+resource)
    conn = http.client.HTTPSConnection(url, timeout=10)
    timeout1=20
    #print("get链接为"+url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.113 Safari/537.36'}
    try:
        conn.request("GET",resource + '/' + params,headers=headers)#,timeout=timeout1
        response = conn.getresponse()
    except requests.exceptions.RequestException as e:
        return "no data"
    except socket.timeout as e:
        return "timeout"

    #print('response='+response)
    data = response.read().decode('utf-8')
    #print('response data='+data)
    return json.loads(data)


#获取K线
def httpGetKline(url,resource,params=''):
    #print('url='+url+'  resource='+resource)
    conn = http.client.HTTPSConnection(url, timeout=10)
    #print("get链接为"+url+resource)
    #conn.request("GET",resource)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.113 Safari/537.36'}
    #conn.request("GET","https://gate.io"+resource)#json_svr/query/?u=10&c=380225&type=kline&symbol=eth_usdt&group_sec=900&range_hour=24")
    #conn.request("GET","https://gate.io/json_svr/query/?u=10&c=380225&type=kline&symbol=eth_usdt&group_sec=900&range_hour=24")
    #response = conn.getresponse().json()
    response=requests.get("http://gate.io"+resource,headers=headers)#json_svr/query/?u=10&c=380225&type=kline&symbol=eth_usdt&group_sec=900&range_hour=24")  
    #print('response='+response)
    #print(response.headers)
    #print('requests 的header='+response.headers)
    data = response.text
    #print("data的类型为",type(data),"内容为",data)
    return data
    #.decode('utf-8')
   
    #return exec(data)


    '''
    json.dumps : dict转成str

    json.loads:str转成dict
    '''



    #print(type(data))

    #data = response.read().decode('utf-8')
    #print('data='+data)

    #dataform = str(data).strip("'<>() ").replace('\0', '')
    #data = response.read().replace('u', '')#.replace('\0', '')
    #data = response.read().decode('utf-8').replace('\\n', '').replace('\\r', '')
    #print('response data='+data)
    #return response
    #return json.dumps(data)
    #return json.loads(data)
    #return json.loads(json.dumps(data))


def httpPost(url,resource,params,apikey,secretkey):
     headers = {
            "Content-type" : "application/x-www-form-urlencoded",
            "KEY":apikey,
            "SIGN":getSign(params,secretkey)
     }
     conn = http.client.HTTPSConnection(url, timeout=10)
     if params:
         temp_params = urllib.parse.urlencode(params)
     else:
         temp_params = ''
     print(temp_params)
     conn.request("POST", resource, temp_params, headers)
     response = conn.getresponse()
     data = response.read().decode('utf-8')
     params.clear()
     conn.close()
     return data


        
     
