# -*- coding: utf-8 -*-
from inquant.util.HttpHelper import *
from inquant.util.LogRecord import *
from inquant.util.DES3Cryptogram import *
from inquant.framework.IBaseDataApi  import *
from inquant.Contract import *
from inquant.AssetInfo import *
import json
import datetime

class FutDataApi(IBaseDataApi):
    """期货数据API"""

    __UrlHeader = "https://stgyapi.inquant.cn/future/"

    def __init__(self):
        """构造函数"""
        super(FutDataApi,self).__init__()

    def GetContract(self,symbol, exchange):
        """获取合约信息"""
        url = self.__UrlHeader + 'Contract/Get?symbol=' + symbol + '&exchange=' + str(int(exchange))
        resp = httpGet(url)
        if not resp:
            self.__wirteError("请求应答为空：" + url)
            return None
        de = decrypt(resp.decode("utf-8"))
        js = json.loads(de,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError(url + js.get('error_info'))
            return None
        data = js.get('data')
        if not data:
            self.__wirteError("data为空：" + url)
            return None
        contract = self.__ToContract(data)
        return contract

    def GetFutContracts(self,varietyCode, exchange, futType):
        """按品种代码获取期货合约"""
        url = self.__UrlHeader + 'Contract/getbyvariety?variety=' + varietyCode + '&exchange=' + str(int(exchange)) + '&futType=' + str(futType)
        resp = httpGet(url)
        if not resp:
            self.__wirteError("请求应答为空：" + url)
            return None
        de = decrypt(resp.decode("utf-8"))
        js = json.loads(de,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError(url + js.get('error_info'))
            return None
        data = js.get('data')
        if not data:
            self.__wirteError("data为空：" + url)
            return None
        contractlist = []
        for item in data:
            contract = self.__ToContract(item)
            contractlist.append(contract)
        return contractlist

    def __ToContract(self,data):
        """根据clientOrderID 获取订单详情"""
        if not data:
            return None
        contract = Contract()
        contract.ContractName = data["contractName"]
        contract.ContractType = ContractType(data["contractType"])
        contract.Currency = Currency(data["currency"])
        contract.Exchange = Exchange(data["exchange"])
        contract.ExpiryDate = datetime.datetime.strptime(data["expiryDate"],'%Y-%m-%d')
        contract.ListingDate = datetime.datetime.strptime(data["listingDate"],'%Y-%m-%d')
        contract.Lots = data["lots"]
        contract.PriceStep = data["priceStep"]
        contract.Right = data["right"]
        contract.StrikePx = data["strikePx"]
        contract.Symbol = data["symbol"]
        contract.ContDetailType = ContDetailType(data["contDetailType"])
        for x in data['tradeTimes']:
            tradingTime = TradingTime()
            tradingTime.Begin = x['begin']
            tradingTime.End = x['end']
            contract.TradingTimes.append(tradingTime)
        return contract

    def __wirteError(self,error):
        '''写错误日志'''
        LogRecord.writeLog('FutDataApiError',error)

if __name__ == '__main__':
    """测试"""
    baseApi = FutDataApi()
    contract = baseApi.GetContract('rb1905',Exchange.SHFE)
    print(contract)

    temp = baseApi.GetFutContracts('rb',Exchange.SHFE,-1)
    print(temp)
