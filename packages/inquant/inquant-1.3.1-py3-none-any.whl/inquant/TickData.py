# -*- coding: utf-8 -*- 

from datetime import *
from inquant.Contract import *

class TickData(object):
    """实时数据模型"""

    def __init__(self):
        """股票代码或合约名称"""
        self.Symbol = ""
        """交易所"""
        self.Exchange = Exchange.UnKnow
        """时间"""
        self.LocalTime = datetime.now()
        """最新成交价"""
        self.LastPx = 0.0
        """成交量"""
        self.Volume = 0
        """持仓量"""
        self.OpenInterest = 0
        """开盘价"""
        self.OpenPx = 0.0
        """最高价"""
        self.HighPx = 0.0
        """最低价"""
        self.LowPx = 0.0
        """昨收"""
        self.PreClosePx = 0.0
        """买N档"""
        self.Bids = []
        """卖N档"""
        self.Asks = []

class LevelUnit(object):
    """一档行情"""

    def __init__(self):
        """价格"""
        self.Px = 0
        """量"""
        self.Vol = 0