# -*- coding: utf-8 -*- 

from datetime import  *  
from enum import IntEnum
from inquant.Contract import *

class Order(object):
    """委托"""

    def __init__(self):
        """策略编号"""
        self.StrategyID = ""
        """委托ID"""
        self.OrderID = ""
        """股票代码或合约代码"""
        self.Symbol = ""
        """交易所"""
        self.Exchange = Exchange.UnKnow
        """委托方向"""
        self.OrderSide = OrderSide.Buy
        """开仓还是平仓 (期货中使用) 非期货为None"""
        self.Offset = Offset.UnKnow
        """委托数量"""
        self.Quantity = 0
        """委托价格"""
        self.Price = 0.0
        """成交数量"""
        self.Filled = 0
        """成交金额"""
        self.FilledPx = 0.0
        """委托时间"""
        self.OrderTime = datetime.now()
        """委托状态"""
        self.Status = OrderStatus.UnKnow
        """委托类型"""
        self.OrderType = OrderType.LMT
        """交易日"""
        self.TradeDate = datetime.now()
        """成交时间"""
        self.FilledTime = datetime.now()
        """委托备注"""
        self.Note = ""

    def IsOpen(self):
        """是否打开的订单"""
        return self.Status != OrderStatus.Cancelled and self.Status != OrderStatus.Filled and self.Status != OrderStatus.Rejected;
     
class OrderType(IntEnum):
        """限价"""
        LMT = 0
        """市价"""
        MKT = 1

class OrderStatus(IntEnum):
        """ 未知""" 
        UnKnow = -1
        """ 未发（下单指令还未发送到下游）"""
        NotSent = 0
        """ 1 已发（下单指令已发送给下游）"""
        Sended = 1
        """ 2 已报（下单指令已报给交易所）"""
        Accepted = 2
        """ 部分成交 """
        PartiallyFilled = 3
        """ 4 已撤（可能已经部分成交，要看看filled字段）"""
        Cancelled = 4
        """ 5 全部成交 """
        Filled = 5
        """ 6 已拒绝 """
        Rejected = 6
        """ 7 撤单请求已发送，但不确定当前状态 """
        PendingCancel = 7

class OrderSide(IntEnum):
        """买入"""
        Buy = ord('B')
        """卖出"""
        Sell = ord('S')

class Offset(IntEnum):
        """未知"""
        UnKnow = 0
        """开仓""" 
        Open = 1
        """平仓 """ 
        Close = 2
        """ 平今 """
        CloseToday = 3
        """ 平昨 """
        CloseYesterday = 4