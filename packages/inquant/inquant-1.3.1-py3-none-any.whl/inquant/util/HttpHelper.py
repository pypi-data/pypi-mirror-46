# -*- coding: utf-8 -*-
import urllib.request

def httpGet(url):
    '''GET请求'''
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0')
    res_data = urllib.request.urlopen(request,timeout=30)
    res = res_data.read()
    return res

def httpPost(reqUrl,args):
    '''FORM表单请求'''
    body = urllib.parse.urlencode({'param':args}).encode('utf-8')
    request = urllib.request.Request(url = reqUrl,data = body)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0')
    res_data = urllib.request.urlopen(request,timeout=30)
    res = res_data.read()
    return res

if __name__ == '__main__':    
    resp = httpGet('https://stgyapi.inquant.cn/future/Contract/Get?symbol=rb1905&exchange=4')
    print(resp)
