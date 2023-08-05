# -*- coding: utf-8 -*- 

from enum import IntEnum
from inquant.Contract import *

class Position(object):
    """持仓信息"""

    def __init__(self):
        """策略编号"""
        self.StrategyID = ""
        """合约代码"""
        self.Symbol = ""
        """交易所"""
        self.Exchange = Exchange.UnKnow
        """持仓数量"""
        self.Quantity = 0
        """冻结数量"""
        self.Frozen = 0
        """持仓成本"""
        self.CostPx = 0.0
        """持仓方向"""
        self.PosSide = PosSide.Net
        """保证金"""
        self.Margin = 0.0

class PosSide(IntEnum):
        """净持仓"""
        Net = 0
        """多仓"""
        Long = 1
        """空仓"""
        Short = 2