# -*- coding: utf-8 -*-
from inquant.framework.IStrategyService import *
from inquant.util.MemCache import *
from inquant.util.LogRecord import *
from inquant.future.FutDataApi import *
from inquant.future.FutMarketApi import *
from inquant.future.FutPaperTradeApi import *
import uuid
import traceback
from queue import Queue
import time

class StrategyService(IStrategyService):
    """策略服务接口"""

    def __init__(self,strategyID,logPath,orderChangedCallback,tickCallback,barCallback):
        """构造函数"""
        super(StrategyService,self).__init__(strategyID,logPath,orderChangedCallback,tickCallback,barCallback)
        self.__strategyID = strategyID
        LogRecord.setLogPath(logPath)
        self.__unhandledQueue = Queue()
        self.__wirteInfo("创建策略:" + strategyID)
        self.__baseDataApi = FutDataApi()
        self.__tickCallback = tickCallback
        self.__barCallback = barCallback
        self.__marketApi = FutMarketApi(self.__OnTick,self.__OnBar)
        self.__tradeApi = FutPaperTradeApi(strategyID,orderChangedCallback)
        self.__wirteInfo("策略创建完成:" + strategyID)
        self.__subscribeList = []
        self.__cache = MemCache()
        #行情状态 0：实时行情 1：回放行情
        self.MarketStatus = 0
        t = threading.Thread(target=self.__StartAutoSub)
        t.start()
        t1 = threading.Thread(target=self.__StartDequeue)
        t1.start()

    def Start(self):
        '''启动策略服务'''
        ret = self.__marketApi.Init(self.__strategyID)
        if not ret:
            self.__wirteError('行情初始化失败')
            return False
        if len(self.__subscribeList) > 0:
            isPlayback = self.MarketStatus == 1
            ret = self.__marketApi.Subscribe(self.__subscribeList, True, isPlayback)
        return True

    def __OnTick(self,tick):
        '''tick行情触发'''
        if not tick:
            return
        self.__unhandledQueue.put(tick)

    def __OnBar(self,bar):
        '''bar行情触发'''
        if not bar:
            return
        self.__unhandledQueue.put(bar)

    def __StartDequeue(self):
        """启动自动订阅"""
        while True:
            try:
                obj = self.__unhandledQueue.get()
                if not obj:
                    time.sleep(0.001)
                    continue
                if isinstance(obj,TickData):
                    key = "{0}.{1}.tick.0".format(obj.Symbol, obj.Exchange)
                    self.__CacheMarket(key,obj)
                    self.__tickCallback(obj)
                elif isinstance(obj,BarData):
                    key = "{0}.{1}.bar.{2}".format(obj.Symbol, obj.Exchange, obj.BarType)
                    self.__CacheMarket(key,obj)
                    self.__barCallback(obj)
            except Exception as e:
                self.__wirteError(str(e))
                self.__wirteError(traceback.format_exc())
                time.sleep(0.001)

    def __CacheMarket(self,key,val):
        '''缓存行情数据'''
        queue = self.__cache.get(key)
        if not queue:
            queue = []
        queue.append(val)
        if len(queue) > 100:
            queue.pop(0)
        #缓存3天
        self.__cache.set(key,queue,60 * 60 * 24 * 3)

    def __StartAutoSub(self):
        """启动自动订阅"""
        while True:
            time.sleep(60)
            try:
                if self.__marketApi.GetStatus() != -1:
                    self.__wirteInfo('后台订阅:' + str(self.GetSubscribeList()),False)
                if len(self.__subscribeList) > 0:
                    ret = self.__marketApi.Subscribe(self.__subscribeList, True, False)
            except Exception as e:
                self.__wirteError(str(e))
                self.__wirteError(traceback.format_exc())

    def GetSubscribeList(self):
        """获取订阅信息"""
        if not self.__subscribeList:
            return []
        data = []
        for x in self.__subscribeList:
            item = '{0}.{1}.{2}.{3}'.format(x.get('symbol'),Exchange(x.get('exchange')).name,x.get('marketType'),x.get('barType'))
            data.append(item)
        return data

    def Subscribe(self,subInfos):
        """行情订阅"""
        if not subInfos:
            return True
        data = []
        for x in subInfos:
            subInfo = self.__ToSubInfo(x)
            if not subInfo:
                self.__wirteError('错误的订阅信息：' + x)
                continue
            if subInfo not in self.__subscribeList:
                self.__subscribeList.append(subInfo)
            data.append(subInfo)
        if self.__marketApi.GetStatus() == -1:#未启动，稍后订阅
            return True
        isPlayback = self.MarketStatus == 1
        self.__marketApi.Subscribe(data,False,isPlayback)

    def __ToSubInfo(self,src):
        '''转化为内部订阅格式'''
        if not src:
            return None
        arr = src.split('.')
        if len(arr) != 4:
            return None
        exchange = Exchange[arr[1].upper()]
        marketType = arr[2].upper()
        barType = int(arr[3])
        return {'symbol':arr[0],'exchange':int(exchange),'marketType':marketType,'barType':barType}

    def Unsubscribe(self,subInfos):
        """取消订阅"""
        if not subInfos:
            return True
        data = []
        for x in subInfos:
            subInfo = self.__ToSubInfo(x)
            if not subInfo:
                self.__wirteError('错误的订阅信息：' + x)
                continue
            if subInfo in self.__subscribeList:
                self.__subscribeList.remove(subInfo)
            data.append(subInfo)
        if self.__marketApi.GetStatus() == -1:#未启动，不必执行
            return True
        self.__marketApi.Unsubscribe(data)

    def GetLastTick(self,symbol, exchange, count):
        """获取最近几笔Tick数据"""
        if not symbol:
            self.__wirteError("合约代码不能为空")
            return None
        tickKey = '{0}.{1}.tick.0'.format(symbol,exchange)
        tickList = self.__cache.get(tickKey)
        if not tickList:
           return []
        start = max(len(tickList) - count,0)
        return tickList[start : start + count]

    def GetLastBar(self,symbol, exchange, barType, count):
        """获取最近几笔Bar数据"""
        if not symbol:
            self.__wirteError("合约代码不能为空")
            return None
        barKey = '{0}.{1}.bar.{2}'.format(symbol,exchange,barType)
        barList = self.__cache.get(barKey)
        if not barList:
           return []
        start = max(len(barList) - count,0)
        return barList[start : start + count]

    def GetHisBar(self,symbol, exchange, barType, startTime, count):
        """获取历史K线数据"""
        return self.__marketApi.GetHisBar(symbol, exchange, barType, startTime, count)

    def SendOrder(self,clientOrderID, symbol, exchange, orderSide, price, quantity, orderType, offset):
        """下单"""
        if not clientOrderID or clientOrderID == '':
            clientOrderID = uuid.uuid1().hex
        ret = self.__tradeApi.SendOrder(clientOrderID, symbol, exchange, orderSide, price, quantity, orderType, offset)
        return ret

    def CancelOrder(self,orderID):
        """撤单"""
        return self.__tradeApi.CancelOrder(orderID)

    def GetAssetInfo(self):
        """获取资产信息"""
        return self.__tradeApi.GetAssetInfo()

    def GetOrder(self,clientOrderID):
        """根据内联ID号 获取订单详情"""
        return self.__tradeApi.GetOrder(clientOrderID)

    def GetOpenOrders(self):
        """获取打开的订单"""
        return self.__tradeApi.GetOpenOrders()

    def GetOrders(self):
        """获取当日委托"""
        return self.__tradeApi.GetOrders()

    def GetPositions(self):
        """获取持仓"""
        return self.__tradeApi.GetPositions()

    def GetContract(self,symbol, exchange):
        """获取合约信息"""
        key = 'ContractBySymbol.' + symbol + str(exchange)
        cache = self.__cache.get(key)
        if cache:
            return cache
        ret = self.__baseDataApi.GetContract(symbol, exchange)
        if not ret:
            return ret
        #30分钟缓存
        self.__cache.set(key,ret,60 * 30)
        return ret

    def GetFutContracts(self,varietyCode, exchange, futType):
        """按品种代码获取期货合约"""
        key = 'ContractByVarietyCode.' + varietyCode + str(exchange) + str(futType)
        cache = self.__cache.get(key)
        if cache:
            return cache
        ret = self.__baseDataApi.GetFutContracts(varietyCode, exchange, futType)
        if not ret:
            return ret
        #30分钟缓存
        self.__cache.set(key,ret,60 * 30)
        return ret

    def WriteLog(self,fileName, log):
        """写日志"""
        LogRecord.writeLog(fileName,log)

    def __wirteError(self,error):
        '''写错误日志'''
        self.WriteLog('StrategyServiceError',error)

    def __wirteInfo(self,info,isPrint = True):
        '''写日志'''
        LogRecord.writeLog('StrategyService',info,isPrint)

