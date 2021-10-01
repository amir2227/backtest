from yahoofinancials import YahooFinancials
import yfinance as yf
from strategys import SmaCross, RSIStrategy
import backtrader
import datetime


ticker = 'BTC-USD'
yahoo_financials = YahooFinancials(ticker)

def get_data(frm,to):
    daily_crypto_prices = yahoo_financials.get_historical_price_data(frm, to, 'daily')

    return daily_crypto_prices['BTC-USD']['prices']
def back(frm,to,balance, st):
    cerebro = backtrader.Cerebro()
    cerebro.broker.set_cash(balance)
    cerebro.broker.setcommission(commission=0.001)
    data = backtrader.feeds.PandasData(dataname=yf.download('BTC-USD', frm, to))        
    cerebro.adddata(data)
    if st == 'both':
        cerebro.addstrategy(RSIStrategy)
        cerebro.addstrategy(SmaCross)
    elif st == 'RSI':
        cerebro.addstrategy(RSIStrategy)
    else:
        cerebro.addstrategy(SmaCross)
    print(f'start value {cerebro.broker.getvalue()}')
    start = f'start value {cerebro.broker.getvalue()}'
    cerebro.run()
    from strategys import res
    res.append(start)
    res.append(f'final value {cerebro.broker.getvalue()}')
    print(f'final value {cerebro.broker.getvalue()}')
    return res

