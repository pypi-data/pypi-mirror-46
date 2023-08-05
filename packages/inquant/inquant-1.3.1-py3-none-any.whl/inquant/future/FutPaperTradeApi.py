# -*- coding: utf-8 -*-
from inquant.util.HttpHelper import *
from inquant.util.LogRecord import *
from inquant.util.MemCache import *
from inquant.util.DES3Cryptogram import *
from inquant.framework.ITradeApi import *
from inquant.Order import *
from inquant.AssetInfo import *
from inquant.Position import *
import json
import time
import uuid
import inquant.util.LogRecord
import datetime
from concurrent.futures.thread import ThreadPoolExecutor

class FutPaperTradeApi(ITradeApi):
    """期货模拟交易"""

    __UrlHeader = "https://stgyapi.inquant.cn/future/papertrade/"

    def __init__(self,strategyID,orderChangedCallback):
        """构造函数"""
        super(FutPaperTradeApi,self).__init__(strategyID,orderChangedCallback)
        self.__strategyID = strategyID
        self.__orderChangedCallback = orderChangedCallback
        self.__cache = MemCache()
        self.__getOrderUrl = self.__UrlHeader + 'getorders?strategyID=' + self.__strategyID
        self.__getAssetUrl = self.__UrlHeader + 'getasset?strategyID=' + self.__strategyID
        self.__getPosUrl = self.__UrlHeader + 'getpositions?strategyID=' + self.__strategyID
        self.__executor = ThreadPoolExecutor(max_workers=1)

    def SendOrder(self,clientOrderID, symbol, exchange, orderSide, price, quantity, orderType, offset):
        """下单"""
        if not symbol or symbol == '':
            self.__wirteError("symbol不能为空")
            return False
        if not isinstance(quantity, int):
            self.__wirteError("quantity必须为整数:{0},{1}".format(quantity,symbol))
            return False
        order = Order()
        order.Exchange = exchange
        order.Filled = 0
        order.FilledPx = 0
        order.FilledTime = datetime.datetime(1970, 1, 1)
        order.Note = ''
        order.Offset = offset
        order.OrderID = clientOrderID
        order.OrderSide = orderSide
        order.OrderTime = datetime.datetime.now()
        order.OrderType = orderType
        order.Price = price
        order.Quantity = quantity
        order.Status = OrderStatus.NotSent
        order.StrategyID = self.__strategyID
        order.Symbol = symbol

        self.__wirteInfo("{0},{1},{2},{3},{4},price:{5},quantity:{6},orderID:{7}".format(symbol, exchange.name, orderSide.name, offset.name, orderType.name, price, quantity, clientOrderID))

        self.__executor.submit(self.__raiseOrderChanged,order)

        param = {'symbol':symbol,'exchange':int(exchange),'orderSide':int(orderSide),'price':price,'quantity':quantity,'orderType':int(orderType),'offset':int(offset),'strategyID':self.__strategyID,'orderID':clientOrderID}
        data = json.dumps(param,ensure_ascii=False)
        en = encrypt(data)
        resp = httpPost(self.__UrlHeader + "sendorder", en)
        de = decrypt(resp.decode("utf-8"))
        js = json.loads(de,encoding='utf-8')

        neworder = Order()
        neworder.Exchange = exchange
        neworder.Filled = 0
        neworder.FilledPx = 0
        neworder.FilledTime = datetime.datetime(1970, 1, 1)
        neworder.Note = ''
        neworder.Offset = offset
        neworder.OrderID = clientOrderID
        neworder.OrderSide = orderSide
        neworder.OrderTime = datetime.datetime.now()
        neworder.OrderType = orderType
        neworder.Price = price
        neworder.Quantity = quantity
        neworder.StrategyID = self.__strategyID
        neworder.Symbol = symbol
        if js.get('error_no') != 0:
            self.__wirteError(data + de)
            neworder.Status = OrderStatus.Rejected
            neworder.Note = js.get('error_info')
        else:
            self.__wirteInfo(data + de)
            neworder.Filled = js["filled"]
            neworder.FilledPx = js["filledPx"]
            neworder.FilledTime = datetime.datetime.strptime(js["filledTime"],'%Y-%m-%d %H:%M:%S')
            neworder.Status = OrderStatus(js["status"])
            neworder.TradeDate = datetime.datetime.strptime(js["tradeDate"],'%Y-%m-%d %H:%M:%S')

        self.__executor.submit(self.__raiseOrderChanged,neworder)
        return True

    def __raiseOrderChanged(self,order):
        '''触发订单改变事件'''
        if not order:
            return
        self.__cache.delete(self.__getOrderUrl)
        self.__cache.delete(self.__getAssetUrl)
        self.__cache.delete(self.__getPosUrl)
        if not self.__orderChangedCallback:
            self.__orderChangedCallback(order)

    def CancelOrder(self,orderID):
        """撤单"""
        self.__wirteError("不支持撤单")
        return False

    def GetAssetInfo(self):
        """获取资产信息"""
        cache = self.__cache.get(self.__getAssetUrl)
        if cache:
            return cache
        resp = httpGet(self.__getAssetUrl)
        if not resp:
            self.__wirteError("请求应答为空：" + self.__getAssetUrl)
            return None
        de = decrypt(resp.decode("utf-8"))
        js = json.loads(de,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError(self.__getAssetUrl + js.get('error_info'))
            return None
        asset = AssetInfo()
        asset.StrategyID = self.__strategyID
        asset.Margin = js['margin']
        asset.Balance = js['balance']
        asset.TotalAsset = asset.Margin + asset.Balance
        asset.Available = asset.Balance
        asset.Currency = Currency.CNY
        #5分钟缓存
        self.__cache.set(self.__getAssetUrl,asset,60 * 5)
        return asset

    def GetOrder(self,clientOrderID):
        """根据内联ID号 获取订单详情"""
        orders = self.GetOrders()
        if not orders:
            None
        for x in orders:
            if x.OrderID == clientOrderID:
                return x
        return None

    def GetOpenOrders(self):
        """获取打开的订单"""
        orders = self.GetOrders()
        if not orders:
            None
        openOrders = []
        for x in orders:
            if x.Status != OrderStatus.Cancelled and x.Status != OrderStatus.Filled and x.Status != OrderStatus.Filled:
                openOrders.append(x)
        return openOrders

    def GetOrders(self):
        """获取当日委托"""
        cache = self.__cache.get(self.__getOrderUrl)
        if cache:
            return cache
        resp = httpGet(self.__getOrderUrl)
        if not resp:
            self.__wirteError("请求应答为空：" + self.__getOrderUrl)
            return None
        de = decrypt(resp.decode("utf-8"))
        js = json.loads(de,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError(self.__getOrderUrl + js.get('error_info'))
            return None
        data = js.get('data')
        if not data:
            return []
        orders = []
        for item in data:
            order = Order()
            order.Exchange = Exchange(item['exchange'])
            order.Filled = item['filled']
            order.FilledPx = item['filledPx']
            order.FilledTime = datetime.datetime.strptime(item['filledTime'],'%Y-%m-%d %H:%M:%S')
            order.Note = item['note']
            order.Offset = Offset(item['offset'])
            order.OrderID = item['orderID']
            order.OrderSide = OrderSide(item['orderSide'])
            order.OrderTime = datetime.datetime.strptime(item['orderTime'],'%Y-%m-%d %H:%M:%S')
            order.OrderType = OrderType(item['orderType'])
            order.Price = item['price']
            order.Quantity = item['quantity']
            order.Status = OrderStatus(item['status'])
            order.Symbol = item['symbol']
            order.TradeDate = datetime.datetime.strptime(item['tradeDate'],'%Y-%m-%d %H:%M:%S')
            order.StrategyID = self.__strategyID
            orders.append(order)
        #5分钟缓存
        self.__cache.set(self.__getOrderUrl,orders,60 * 5)
        return orders

    def GetPositions(self):
        """获取持仓"""
        cache = self.__cache.get(self.__getPosUrl)
        if cache:
            return cache
        resp = httpGet(self.__getPosUrl)
        if not resp:
            self.__wirteError("请求应答为空：" + self.__getPosUrl)
            return None
        de = decrypt(resp.decode("utf-8"))
        js = json.loads(de,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError(self.__getPosUrl + js.get('error_info'))
            return None
        data = js.get('data')
        if not data:
            return []
        posList = []
        for item in data:
            pos = Position()
            pos.Exchange = Exchange(item['exchange'])
            pos.Frozen = item['frozen']
            pos.Margin = item['margin']
            pos.PosSide = PosSide(item['posSide'])
            pos.Quantity = item['quantity']
            pos.Symbol = item['symbol']
            pos.CostPx = item['costPx']
            pos.StrategyID = self.__strategyID
            posList.append(pos)
        #5分钟缓存
        self.__cache.set(self.__getPosUrl,posList,60 * 5)
        return posList

    def __wirteError(self,error):
        '''写错误日志'''
        LogRecord.writeLog('FutPaperTradeApiError',error)

    def __wirteInfo(self,info):
        '''写日志'''
        LogRecord.writeLog('FutPaperTradeApi',info)

if __name__ == '__main__':
    """测试"""
    try:
        LogRecord.setLogPath("d:/logs/")
        trade = FutPaperTradeApi('2-xk1211231243242314123534523453',None)
        orderId = uuid.uuid1().hex
        a1 = trade.SendOrder(orderId,'rb1905',Exchange.SHFE,OrderSide.Buy,0,1,OrderType.MKT,Offset.Open)
        a2 = trade.CancelOrder(orderId)
        a3 = trade.GetAssetInfo()
        a4 = trade.GetOpenOrders()
        a5 = trade.GetOrder(orderId)
        a6 = trade.GetOrders()
        a7 = trade.GetPositions()
    except Exception as e:
        print(e)
    pass
