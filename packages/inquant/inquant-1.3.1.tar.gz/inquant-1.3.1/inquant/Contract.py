# -*- coding: utf-8 -*- 

from datetime import *
from enum import IntEnum
from inquant.AssetInfo import Currency

class Contract(object):
    """合约信息"""

    def __init__(self):
        """代码"""
        self.Symbol = ""

        """名称"""
        self.ContractName = ""

        """交易所"""
        self.Exchange = Exchange.UnKnow

        """投资品种类型"""
        self.ContractType = ContractType.UnKnow

        """合约细分类型"""
        self.ContDetailType = ContDetailType.Default

        """每股手数"""
        self.Lots = 1

        """最小价差"""
        self.PriceStep = 0

        """到期日"""
        self.ExpiryDate = datetime.now()

        """行权价"""
        self.StrikePx = 0.0

        """期权类型 P:Put C:Call"""
        self.Right = ""

        """上市日期"""
        self.ListingDate = datetime.now()

        """币种"""
        self.Currency = Currency.CNY

        """交易时间"""
        self.TradingTimes = []

class TradingTime(object):
    """交易时间"""

    def __init__(self):
        """开始时间"""
        self.Begin = ""

        """结束时间"""
        self.End = ""

class ContractType(IntEnum):
        """合约类型"""

        """未知"""
        UnKnow = 0
        """股票"""
        Stock = 1
        """期货"""
        Future = 2
        """期权"""
        Option = 3

class ContDetailType(IntEnum):
        """合约细分类型"""

        """常规合约"""
        Default = 1
        """主连合约"""
        Main = 2
        """指数合约"""
        Index = 3

class Exchange(IntEnum):
        """交易所"""

        """未知"""
        UnKnow = 0
        """上交所"""
        SHSE = 1
        """深交所"""
        SZSE = 2
        """中金所"""
        CFFEX = 3
        """上期所"""
        SHFE = 4
        """大商所"""
        DCE = 5
        """郑商所"""
        CZCE = 6
        """港交所"""
        HKSE = 7
        """纳斯达克"""
        NASDAQ = 8
        """纽约证券交易所"""
        NYSE = 9
        """全美证券交易所"""
        AMEX = 10
        """新三板"""
        SBSE = 11
        """伦敦商品交易所"""
        LME = 12
        """马来西亚衍生产品交易所"""
        BMD = 13
        """东京商品交易所"""
        TOCOM = 14
        """上海国际能源交易中心"""
        INE = 15