# -*- coding: utf-8 -*-
class IMarketApi(object):
    """行情接口"""

    def __init__(self,tickCallback,barCallback):
        """构造函数"""
        pass

    def Init(self,strategyID):
        """初始化"""
        pass

    def GetStatus(self):
        """状态 -1:未初始化 0:正常 1:已断开"""
        pass

    def Subscribe(self,subInfos, isClear, isPlayback):
        """行情订阅"""
        pass

    def Unsubscribe(self,subInfos):
        """取消订阅"""
        pass

    def GetHisBar(self,symbol, exchange, barType, startTime, count):
        """获取历史K线数据"""
        pass

