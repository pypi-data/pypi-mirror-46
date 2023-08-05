# -*- coding: utf-8 -*-
class IStrategyService(object):
    """策略服务接口"""

    def __init__(self,strategyID,logPath,orderChangedCallback,tickCallback,barCallback):
        """构造函数"""
        #行情状态 0：实时行情 1：回放行情
        self.MarketStatus = 0
        pass

    def GetSubscribeList(self):
        """获取订阅信息"""
        pass

    def Subscribe(self,subInfos):
        """行情订阅"""
        pass

    def Unsubscribe(self,subInfos):
        """取消订阅"""
        pass

    def GetLastTick(self,symbol, exchange, count):
        """获取最近几笔Tick数据"""
        pass

    def GetLastBar(self,symbol, exchange, barType, count):
        """获取最近几笔Bar数据"""
        pass

    def GetHisBar(self,symbol, exchange, barType, startTime, count):
        """获取历史K线数据"""
        pass

    def SendOrder(self,clientOrderID, symbol, exchange, orderSide, price, quantity, orderType, offset):
        """下单"""
        pass

    def CancelOrder(self,orderID):
        """撤单"""
        pass

    def GetAssetInfo(self):
        """获取资产信息"""
        pass

    def GetOrder(self,clientOrderID):
        """根据内联ID号 获取订单详情"""
        pass

    def GetOpenOrders(self):
        """获取打开的订单"""
        pass

    def GetOrders(self):
        """获取当日委托"""
        pass

    def GetPositions(self):
        """获取持仓"""
        pass

    def GetContract(self,symbol, exchange):
        """获取合约信息"""
        pass

    def GetFutContracts(self,varietyCode, exchange, futType):
        """按品种代码获取期货合约"""
        pass

    def WriteLog(self,fileName, log):
        """写日志"""
        pass

