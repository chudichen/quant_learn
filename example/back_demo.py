"""
数据回测
"""
import backtrader as bt
import data.stock as st
import datetime


def get_data():
    df = st.get_csv_price('300750.XSHE')
    return df


class TestStrategy(bt.Strategy):
    params = (
        ('ma_period', 15),
    )

    # noinspection PyArgumentList
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        self.max_price = None
        self.profit = None

        # 计算10日均线
        self.sma5 = bt.indicators.MovingAverageSimple(self.dataclose, period=5)
        # 计算30日均线
        self.sma1 = bt.indicators.MovingAverageSimple(self.dataclose, period=1)
        # self.sma120 = bt.indicators.MovingAverageSimple(self.dataclose, period=120)

        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
        #                                     subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 处于正在买和卖的状态时不做处理
            return
        # 检查订单是否完成，如果余额不足时，可能交易被交易商拒绝
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buy_price = order.executed.price
                self.buy_comm = order.executed.comm
                self.max_price = self.buy_price
                self.profit = - self.buy_comm
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            # noinspection PyAttributeOutsideInit
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        # 有交易中订单则返回
        if self.order:
            return

        # # 无持仓，买入策略
        if not self.position:
            if self.sma1[0] > self.sma1[-1] > self.sma1[-2] and self.sma5[0] > self.sma5[-1]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()
        # 有持仓，卖出策略
        else:
            # 有收益保本模式
            if self.profit > 0:
                if (self.max_price - self.profit) / self.max_price > 0.1:
                    self.sell()

            # 无收益止损模式
            else:
                if (self.max_price - self.profit) / self.max_price > 0.15:
                    self.sell()

        # # 没有持仓
        # if not self.position:
        #     if self.sma5[0] > self.sma10[0] and self.sma5[-1] < self.sma10[-1]:
        #         self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #         self.buy()
        # else:
        #     # 已经持仓
        #     if self.sma5[0] < self.sma10[0] and self.sma5[-1] > self.sma10[-1]:
        #         self.log('SELL CREATE, %.2f' % self.dataclose[0])
        #         self.order = self.sell()


if __name__ == '__main__':
    # 初始化引擎
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    cerebro.broker.setcommission(commission=0.001)
    df = get_data()
    # noinspection PyArgumentList
    data = bt.feeds.PandasData(dataname=df, fromdate=datetime.datetime(2021, 1, 1))
    cerebro.adddata(data)

    # 默认初始资金为10K，设置初始资金：
    cerebro.broker.setcash(100000.0)
    print('初始市值: %.2f' % cerebro.broker.getvalue())

    # 回测启动运行
    result = cerebro.run()
    print('期末市值: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
