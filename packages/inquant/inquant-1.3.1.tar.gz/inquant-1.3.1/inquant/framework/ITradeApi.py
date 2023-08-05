# -*- coding: utf-8 -*-
class ITradeApi(object):
    """交易接口"""

    def __init__(self,strategyID,orderChangedCallback):
        """构造函数"""
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


