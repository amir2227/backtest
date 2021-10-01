import backtrader as bt
import datetime

res=[]


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=50,  # period for the fast moving average
        pslow=200   # period for the slow moving average
    )
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        res.append(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
       
        if self.crossover > 0:  # if fast crosses slow to the upside
        
            self.close()
            self.log(self.position)
            self.buy() # enter long
            self.log("SMA Buy signal {} shares".format( self.data.close[0]))
            self.log(self.position)
                
 
        elif self.crossover < 0:  # in the market & cross to the downside
           
            self.close()# close long position
            self.log(self.position)
            self.sell()
            self.log("SMA Sale signal {} shares".format(self.data.close[0]))
            self.log(self.position)
            

class RSIStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        res.append(f'{dt.isoformat()}, {txt}')
        
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.pos = False

        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=15)
        self.rsi = bt.indicators.RelativeStrengthIndex()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        #self.log('Close, %.2f' % self.dataclose[0])
        
        if self.order:
            return

        if not self.pos:
            if (self.rsi[0] < 30):
                self.log(f'rsi: {self.rsi[0]}')
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy(size=1)
                self.pos = True

        else:
            if (self.rsi[0] > 70):
                self.log(f'rsi: {self.rsi[0]}')
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell(size=1)
                self.pos = False
    
