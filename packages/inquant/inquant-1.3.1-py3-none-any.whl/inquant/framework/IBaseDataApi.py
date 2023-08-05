# -*- coding: utf-8 -*-
class IBaseDataApi(object):
    """基础数据接口"""

    def __init__(self):
        """构造函数"""
        pass

    def GetContract(self,symbol, exchange):
        """获取合约信息"""
        pass

    def GetFutContracts(self,varietyCode, exchange, futType):
        """按品种代码获取期货合约"""
        pass

