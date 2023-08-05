# -*- coding: utf-8 -*-
from inquant import *

class MyStrategy(StrategyTemplate):
    """我的策略"""

    def __init__(self,strategyID,logPath):
        """构造函数"""
        super(MyStrategy,self).__init__(strategyID,logPath)
        self.isfirst = 0

    def OnTick(self, data):
        """Tick数据处理 注data参数一次只有一条tick数据"""
        #time.sleep(1)
        self.WriteInfo('tick : {0} {1} {2}'.format(data.Symbol,data.LocalTime,data.Exchange))
        pass

    def OnBar(self, data):
        """Bar数据处理 注data参数一次只有一条bar数据"""
        self.WriteInfo('bar : {0} {1} {2}'.format(data.Symbol,data.LocalTime,data.Exchange))

        resp10 = strategy.GetLastBar(data.Symbol,data.Exchange,data.BarType,10)

        if self.isfirst == 0:
            self.isfirst = 1
            resp4 = self.SendOrder(data.Symbol,data.Exchange,OrderSide.Sell,data.LastPx,1,OrderType.LMT,Offset.Close)
        pass

    def OnOrderChanged(self,order):
        """成交回报处理"""
        self.WriteInfo('OrderChanged : {0} {1} {2}'.format(order.Symbol,order.Price,order.Exchange))
        pass

    def TaskCallback(self):

        self.Unsubscribe(["j1909.DCE.TICK.0", "j1909.dce.bar.60"])

if __name__ == '__main__':
    #新建策略
    strategy = MyStrategy('2-xk1211231243242314123534523453','/home/admin/logs/测试策略/')
    strategy.SetMarketStatus(1)

    ret = strategy.GetHisBar("j1905",Exchange.DCE,60 * 60,1000)

    #创建定时任务
    strategy.CreateScheduler(strategy.TaskCallback, [95830, 95855, 164300])

    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,-1)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,0)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,1)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,2)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,3)

    strategy.Subscribe(["jmM.dce.TiCk.0", "jmM.DCE.BAR.60"])
    strategy.Subscribe(["j1909.DCE.Tick.0", "j1909.DCE.BAR.60"])

    strategy.WriteInfo(u"开始启动策略...")
    resp = strategy.Start()
    if not resp:
        strategy.WriteError(u"策略启动失败！！")
        input(u"按任意键退出")
        sys.exit()
    strategy.WriteInfo(u"策略启动成功")

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

    input(u"策略执行中，按任意键退出...")