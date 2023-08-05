# -*- coding: utf-8 -*-
from inquant import *

class MyStrategy(StrategyTemplate):
    """�ҵĲ���"""

    def __init__(self,strategyID,logPath):
        """���캯��"""
        super(MyStrategy,self).__init__(strategyID,logPath)
        self.isfirst = 0

    def OnTick(self, data):
        """Tick���ݴ��� עdata����һ��ֻ��һ��tick����"""
        self.WriteInfo('tick : {0} {1} {2}'.format(data.Symbol,data.LocalTime,data.Exchange))
        pass

    def OnBar(self, data):
        """Bar���ݴ��� עdata����һ��ֻ��һ��bar����"""
        self.WriteInfo('bar : {0} {1} {2}'.format(data.Symbol,data.LocalTime,data.Exchange))

        resp10 = strategy.GetLastBar(data.Symbol,data.Exchange,data.BarType,5)

        if self.isfirst == 0:
            self.isfirst = 1
            resp4 = self.SendOrder(data.Symbol,data.Exchange,OrderSide.Sell,data.LastPx,1,OrderType.LMT,Offset.Close)
        pass

    def OnOrderChanged(self,order):
        """�ɽ��ر�����"""
        self.WriteInfo('OrderChanged : {0} {1} {2}'.format(order.Symbol,order.Price,order.Exchange))
        pass

    def TaskCallback(self):
        print(datetime.now().time())

if __name__ == '__main__':
    #�½�����
    strategy = MyStrategy('2-xk1211231243242314123534523453','/home/admin/logs/���Բ���/')

    strategy.SetMarketStatus(1)

    ret = strategy.GetHisBar("rb1905",Exchange.SHFE,60 * 60,1000,20181015150000)

    #������ʱ����
    strategy.CreateScheduler(strategy.TaskCallback,[90000,161005])

    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,-1)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,0)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,1)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,2)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,3)

    a1 = strategy.Subscribe(["rbM.SHFE.Tick.0", "rbM.SHFE.Bar.300"])

    strategy.WriteInfo(u"��ʼ��������...")
    resp = strategy.Start()
    if not resp:
        strategy.WriteError(u"��������ʧ�ܣ���")
        input(u"��������˳�")
        sys.exit()
    strategy.WriteInfo(u"���������ɹ�")

    resp4 = strategy.SendOrder('rb1905',Exchange.SHFE,OrderSide.Buy,0,1,OrderType.MKT,Offset.Open)
    resp5 = strategy.CancelOrder('7ba0ab1c8319442299c835269f600f3f')

    resp1 = strategy.GetAssetInfo()
    resp2 = strategy.GetOrders()
    resp3 = strategy.GetPositions()
        
    resp6 = strategy.GetOrder('7ba0ab1c8319442299c835269f600f3f')
    resp7 = strategy.GetOpenOrders()
    resp8 = strategy.GetContract('rb1905',Exchange.SHFE)
    resp9 = strategy.GetLastTick('rb1905',Exchange.SHFE,2)
    resp10 = strategy.GetLastBar('rb1905',Exchange.SHFE,300,5)

    input(u"����ִ���У���������˳�...")