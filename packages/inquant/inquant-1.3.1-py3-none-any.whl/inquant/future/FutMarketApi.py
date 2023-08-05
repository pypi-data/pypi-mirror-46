# -*- coding: utf-8 -*-
from inquant.util.HttpHelper import *
from inquant.util.LogRecord import *
from inquant.Contract import *
from inquant.TickData import *
from inquant.BarData import *
from inquant.util.DES3Cryptogram import *
from inquant.util.LongTcpClient import *
from inquant.framework.IMarketApi import *
import json
import time
import uuid
import inquant.util.LogRecord
import datetime
import traceback

class FutMarketApi(IMarketApi):
    """行情接口"""

    #行情地址
    __host = 'futquantpush.inquant.cn'

    #端口
    __port = 8986

    #行情包头
    __PACKET_HEADER = 'IQHQ'


    def __init__(self,tickCallback,barCallback):
        """构造函数"""
        super(FutMarketApi,self).__init__(tickCallback,barCallback)
        self.__tickCallback = tickCallback
        self.__barCallback = barCallback
        self.__clinet = None

    def Init(self,strategyID):
        """初始化"""
        if self.__clinet:
            return True
        self.__strategyID = strategyID

        self.__clinet = LongTcpClient(self.__host,self.__port,self.__PACKET_HEADER,self.__OnRecv,self.__OnError)
        self.__wirteInfo("开始连接{0}:{1}".format(self.__host,self.__port))
        if not self.__clinet.Connect():
            self.__wirteError("行情连接失败{0}:{1}".format(self.__host,self.__port))
            return False
        self.__wirteInfo("期货行情服务器连接成功")

        self.__clinet.StartAutoReconnect()
        self.__wirteInfo("启动自动重连")

        heartbeat = {"msgType":"0","content":"python"}
        data = json.dumps(heartbeat,ensure_ascii=False)
        enhb = encrypt(data)
        self.__clinet.StartHeartBeat(enhb)
        return True

    def __OnRecv(self,msg):
        '''收到行情消息'''
        if not msg:
            return
        arr = msg.split(chr(0))
        if len(arr) <= 0:
            return
        if arr[0] == '99':
            tick = self.__ToTickData(arr)
            if not tick:
                return
            if self.__tickCallback:
                self.__tickCallback(tick)
        elif arr[0] == '100':
            bar = self.__ToBarData(arr)
            if not bar:
                return
            if self.__barCallback:
                self.__barCallback(bar)

    def __ToBarData(self,arr):
        #消息长度可能会增加
        if not arr or len(arr) < 11:
            return None
        barData = BarData()
        barData.Symbol = arr[1]
        barData.Exchange = Exchange(int(arr[2]))
        barData.BarType = arr[3]
        barData.LocalTime = datetime.datetime.strptime(arr[4],'%Y%m%d%H%M%S') 
        barData.LastPx = float(arr[5])
        barData.OpenPx = float(arr[6])
        barData.HighPx = float(arr[7])
        barData.LowPx = float(arr[8])
        barData.PreClosePx = float(arr[9])
        barData.Volume = int(arr[10])
        return barData

    def __ToTickData(self,arr):
        if not arr or len(arr) < 13:
            return None
        tick = TickData()
        tick.Symbol = arr[1]
        tick.Exchange = Exchange(int(arr[2]))
        tick.LocalTime = datetime.datetime.strptime(arr[3],'%Y%m%d%H%M%S') 
        tick.LastPx = float(arr[4])
        tick.OpenPx = float(arr[5])
        tick.HighPx = float(arr[6])
        tick.LowPx = float(arr[7])
        tick.PreClosePx = float(arr[8])
        tick.Volume = int(arr[9])
        tick.OpenInterest = int(arr[10])
        bids = json.loads(arr[11],encoding='utf-8')
        for x in bids:
            unit = LevelUnit()
            unit.Px = float(x['px'])
            unit.Vol = int(x['vol'])
            tick.Bids.append(unit)
        asks = json.loads(arr[12],encoding='utf-8')
        for x in asks:
            unit = LevelUnit()
            unit.Px = float(x['px'])
            unit.Vol = int(x['vol'])
            tick.Asks.append(unit)
        return tick

    def __OnError(self,excp):
        '''发生错误时触发'''
        if not excp:
            return
        log = str(excp)
        log += traceback.format_exc()
        self.__wirteError(log)

    def GetStatus(self):
        """状态 -1:未初始化 0:正常 1:已断开"""
        if self.__clinet:
            return 0
        return -1

    def Subscribe(self,subInfos, isClear, isPlayback):
        """行情订阅"""
        if not self.__clinet:
            self.__wirteError('行情未初始化')
            return False
        if not subInfos:
            self.__wirteError('订阅参数不能为空')
            return False
        reqId = uuid.uuid1().hex
        contracts = json.dumps(subInfos,ensure_ascii=False)
        clear = 0
        if isClear:
            clear = 1
        playback = 0
        if isPlayback:
            playback = 1
        param = {"msgType":1,"reqID":reqId,"strategyID":self.__strategyID,"contracts":contracts,"isClear":clear,"isPlayback":playback}
        data = json.dumps(param,ensure_ascii=False)
        en = encrypt(data)
        if not self.__clinet.Send(en):
            self.__wirteError('订阅消息发送失败')
            return False
        return True

    def Unsubscribe(self,subInfos):
        """取消订阅"""
        if not self.__clinet:
            self.__wirteError('行情未初始化')
            return False
        if not subInfos:
            self.__wirteError('订阅参数不能为空')
            return False
        reqId = uuid.uuid1().hex
        contracts = json.dumps(subInfos,ensure_ascii=False)
        param = {"msgType":2,"reqID":reqId,"strategyID":self.__strategyID,"contracts":contracts}
        data = json.dumps(param,ensure_ascii=False)
        en = encrypt(data)
        if not self.__clinet.Send(en):
            self.__wirteError('订阅消息发送失败')
            return False
        return True

    def GetHisBar(self,symbol, exchange, barType, startTime, count):
        """获取历史K线数据"""
        if not symbol:
            self.__wirteError("合约代码不能为空")
            return None
        klineType = self.__ToKlineType(barType)
        if not klineType:
            self.__wirteError("不支持的BarType：" + klineType)
            return None
        url = 'https://hq.inquant.cn/hqfut/quant/getkline.ashx?symbol={0}&exchange={1}&count={2}&type={3}&endTime={4}&isLastKLine=1'.format(symbol,exchange, count, klineType, startTime)
        resp = httpGet(url)
        if not resp:
            self.__wirteError("请求应答为空：" + url)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('code') != 0:
            self.__wirteError(url + js.get('info'))
            return None
        data = js.get('data')
        if not data:
            self.__wirteError("data为空：" + url)
            return None
        result = []
        for x in data:
            bar = BarData()
            bar.BarType = barType
            bar.Symbol = symbol
            bar.Exchange = exchange
            bar.HighPx = abs(float(x['high']))
            bar.LastPx = abs(float(x['lastPx']))
            bar.LocalTime = datetime.datetime.strptime(x['timeStamp'],'%Y%m%d%H%M%S')
            bar.LowPx = abs(float(x['low']))
            bar.OpenPx = abs(float(x['open']))
            bar.PreClosePx = abs(float(x['close']))
            bar.Volume = int(x['vol'])
            result.append(bar)
        return result

    def __ToKlineType(self,barType):
        '''转化为内部类型'''
        if barType == 60:
            return 1
        elif barType == 5 * 60:
            return 2
        elif barType == 15 * 60:
            return 3
        elif barType == 30 * 60:
            return 4
        elif barType == 60 * 60:
            return 5
        elif barType == 24 * 60 * 60:
            return 6
        elif barType == 7 * 24 * 60 * 60:
            return 7
        elif barType == 30 * 24 * 60 * 60:
            return 8
        elif barType == 365 * 24 * 60 * 60:
            return 9
        return None

    def __wirteError(self,error):
        '''写错误日志'''
        LogRecord.writeLog('FutMarketApiError',error)

    def __wirteInfo(self,info):
        '''写日志'''
        LogRecord.writeLog('FutMarketApi',info)

if __name__ == '__main__':
    """测试"""
    try:
        LogRecord.setLogPath("d:/logs/")
        market = FutMarketApi(None,None)
        a1 = market.Init('2-xk1211231243242314123534523453')
        a2 = market.Subscribe([{'symbol':'rb1905','exchange':4,'marketType':'TICK','barType':0},{'symbol':'rb1905','exchange':4,'marketType':'BAR','barType':300}],True,True)
        a3 = market.Unsubscribe([{'symbol':'rb1906','exchange':4,'marketType':'TICK','barType':0}])
        time.sleep(5)
        a4 = market.GetLastTick('rb1905',Exchange.SHFE,10)
        a5 = market.GetLastBar('rb1905',Exchange.SHFE,5 * 60,1000)
        a6 = market.GetHisBar('rb1905',Exchange.SHFE,5 * 60,20190101120000,1000)
    except Exception as e:
        print(e)
    pass
