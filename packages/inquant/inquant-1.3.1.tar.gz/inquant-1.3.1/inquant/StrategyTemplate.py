# -*- coding: utf-8 -*-
from inquant.framework.StrategyService import *
import time
import datetime

class StrategyTemplate(object):
    """
    策略模板
    """
    def __init__(self,strategyID,logPath):
        """构造函数"""
        #策略服务
        self.__strategyService = StrategyService(strategyID,logPath,self.__OnOrderChanged,self.__OnTick,self.__OnBar)

    def GetMarketStatus(self):
        '''获取行情状态'''
        return self.__strategyService.MarketStatus

    def SetMarketStatus(self,marketStatus):
        '''设置行情状态  0：实时行情 1：回放行情'''
        self.__strategyService.MarketStatus = marketStatus

    def GetSubscribeList(self):
        '''获取订阅信息'''
        return self.__strategyService.GetSubscribeList()

    def CreateScheduler(self,schedulerFunc,times):
        """创建定时任务
        schedulerFunc : 定时任务回调函数
        times : 定时触发时间，如[90000,161005]，每日9点0分0秒和16点10分5秒触发schedulerFunc"""
        if not schedulerFunc or not times:
            return False
        t = threading.Thread(target=self.__SchedulerCallback,args=(schedulerFunc,times,))
        t.setDaemon(True)
        t.start()

    def __SchedulerCallback(self,schedulerFunc,times):
        """定时任务回调"""
        if not schedulerFunc or not times:
            return

        preExecTime = 0
        while(True):
            try:
                timeStr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                currTime = int(timeStr)
                if (preExecTime != currTime and currTime % 1000000 in times):
                    self.WriteInfo("run scheduler:" + timeStr)
                    preExecTime = currTime
                    schedulerFunc()
            except Exception as e:
                self.WriteError(str(e),True)
            time.sleep(0.2)

    def Start(self):
        """启动"""
        return self.__strategyService.Start()

    def Subscribe(self,subInfos):
        """行情订阅 [ "rbM.SHFE.TICK.0","rbM.SHFE.BAR.60"]"""
        return self.__strategyService.Subscribe(subInfos)

    def Unsubscribe(self,subInfos):
        """取消订阅 [ "rbM.SHFE.TICK.0","rbM.SHFE.BAR.60"]"""
        return self.__strategyService.Unsubscribe(subInfos)

    def SendOrder(self, symbol, exchange, orderSide, price, quantity, orderType, offset=Offset.UnKnow, clientOrderID=''):
        """发送委托请求"""
        return self.__strategyService.SendOrder(clientOrderID, symbol, exchange, orderSide, price, quantity, orderType, offset)

    def CancelOrder(self,orderID):
        """撤单"""
        return self.__strategyService.CancelOrder(orderID)

    def GetAssetInfo(self):
        """查询资产信息"""
        return self.__strategyService.GetAssetInfo()
    
    def GetOrder(self,clientOrderID):
        """根据clientOrderID 获取订单详情"""
        return self.__strategyService.GetOrder(clientOrderID)

    def GetOpenOrders(self):
        """获取打开的订单"""
        return self.__strategyService.GetOpenOrders()

    def GetOrders(self):
        """获取当日委托"""
        return self.__strategyService.GetOrders()

    def GetPositions(self):
        """查询当前持仓"""
        return self.__strategyService.GetPositions()

    def GetContract(self,symbol, exchange):
        """获取证券基本信息"""
        return self.__strategyService.GetContract(symbol, exchange)

    def GetFutContracts(self,varietyCode, exchange, futType):
        """根据品种代码获取证券基本信息
        varietyCode : 品种代码
        exchange : 交易所
        contDetailType : 期货合约类型 -1:获取所有合约 0:获取主力合约 1:常规合约 2:主连合约 3:指数合约"""
        return self.__strategyService.GetFutContracts(varietyCode, exchange, futType)
    
    def GetLastTick(self, symbol, exchange, count=1):
        """获取最近几笔TICK行情"""
        return self.__strategyService.GetLastTick(symbol,exchange,count)

    def GetLastBar(self, symbol, exchange, barType, count=1):
        """获取最近几笔BAR行情"""
        return self.__strategyService.GetLastBar(symbol,exchange,barType,count)

    def GetHisBar(self, symbol, exchange, barType, count, startTime=None):
        """获取历史行情数据
        symbol : 品种代码
        exchange : 交易所
        barType : K线类型，以秒为单位（1分钟:60 5分钟:6*60 15分钟:15*60 30分钟:30*60 60分钟:60*60 日:24*60*60 月:30*24*60*60 年:365*24*60*60）
        count : K线数量
        startTime : 起始时间:%Y%m%d%H%M%S """

        if not startTime:
            startTime = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        return self.__strategyService.GetHisBar(symbol,exchange,barType,startTime,count)

    def WriteError(self, log, islogtrace=False):
        """写错误日志"""
        self.__strategyService.WriteLog("strategyError", log)
        if islogtrace:
            tracelog = traceback.format_exc()
            self.__strategyService.WriteLog("strategyError", tracelog)

    def WriteInfo(self, log):
        """写一般日志"""
        print(log)
        self.__strategyService.WriteLog("strategy", log)

    def OnBar(self,bar):
        """当有Bar数据推送来的时候做的处理"""
        pass

    def OnTick(self,tick):
        """当有Tick数据推送来的时候做的处理"""
        pass

    def OnOrderChanged(self,order):
        """当有成交回报推送来的时候做的处理"""
        pass

    def __OnTick(self, tick): 
        """Net类型转化为Python类型"""
        if tick == None:
            return
        try:
            self.OnTick(tick)
        except Exception as e:
            self.WriteError(str(e),True) 

    def __OnBar(self,bar):
        """Net类型转化为Python类型"""
        if bar == None:
            return
        try:
            self.OnBar(bar)
        except Exception as e:
            self.WriteError(str(e),True)

    def __OnOrderChanged(self,order):
        """Net类型转化为Python类型"""
        if order == None:
            return
        try:
            self.OnOrderChanged(order)
        except Exception as e:
            self.WriteError(str(e),True)

if __name__ == '__main__':
   
    strategy = StrategyTemplate('2-xk1211231243242314123534523453','/home/admin/logs/测试策略/')

    strategy.SetMarketStatus(1);

    ret = strategy.GetHisBar("rb1901",Exchange.SHFE,60 * 60,1000,20181015150000)

    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,-1)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,0)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,1)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,2)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,3)

    a1 = strategy.Subscribe([ "rbM.SHFE.Tick.0", "rbM.SHFE.Bar.300" ])

    strategy.WriteInfo(u"开始启动策略...")
    resp = strategy.Start()
    if not resp:
        strategy.WriteError(u"策略启动失败！！")
        input(u"按任意键退出")
        sys.exit()
    strategy.WriteInfo(u"策略启动成功")

    resp4 = strategy.SendOrder('rb1901',Exchange.SHFE,OrderSide.Buy,4166,1.0,OrderType.LMT,Offset.Open)
    resp5 = strategy.CancelOrder('7ba0ab1c8319442299c835269f600f3f')

    resp1 = strategy.GetAssetInfo()
    resp2 = strategy.GetOrders()
    resp3 = strategy.GetPositions()
        
    resp6 = strategy.GetOrder('7ba0ab1c8319442299c835269f600f3f')
    resp7 = strategy.GetOpenOrders()
    resp8 = strategy.GetContract('rb1901',Exchange.SHFE)
    resp9 = strategy.GetLastTick('rb1901',Exchange.SHFE,2)
    resp10 = strategy.GetLastBar('rb1901',Exchange.SHFE,300,5)

    input(u"策略执行中，按任意键退出...")
