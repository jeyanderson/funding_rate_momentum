import ccxt
import pandas as pd
from math import floor

ftx=ccxt.ftx({
            "apiKey":'apiKey',
            "secret":'secretKey',
            'headers':{
                'FTX-SUBACCOUNT':'subaccountName'
            }
        })
positions=ftx.fetch_positions()
for i in positions:
    if float(i['info']['size'])>0:
        netSize=i['info']['netSize']
        symbol=i['info']['future']
        netSize=float(netSize)
        if netSize<0:
            ftx.create_market_buy_order(symbol,abs(netSize))
        else:
            ftx.create_market_sell_order(symbol,netSize)
markets=ftx.load_markets()
markets=pd.DataFrame(markets)
markets=markets.T
markets=markets[markets['id'].str.contains('-PERP')]
symbols=markets['id'].to_list()
volumes=[]
fundingRates=[]
for symbol in symbols:
    orders=ftx.fetch_open_orders(symbol)
    if len(orders):
        ftx.cancel_order(int(orders[0]['info']['id']),symbol)
    fr=ftx.fetch_funding_rate(symbol)
    volumes.append(fr['info']['volume'])
    fundingRates.append(fr['info']['nextFundingRate'])
fullDf={
    'symbol':symbols,
    'volume':volumes,
    'fundingRate':fundingRates
}
fullDf=pd.DataFrame(fullDf)
fullDf[['volume','fundingRate']]=fullDf[['volume','fundingRate']].apply(pd.to_numeric)
fullDf=fullDf[fullDf['volume'] >= fullDf['volume'].quantile(.75)]
lowerDf=fullDf.nsmallest(5,'fundingRate')
highDf=fullDf.nlargest(5,'fundingRate')
balance=ftx.fetch_balance({'currency':'usd'})
balance=float(balance['info']['result'][0]['total'])
portion=floor(balance/10)
for symbol in lowerDf['symbol']:
    price=ftx.fetch_ticker(symbol)
    price=float(price['ask'])
    size=float(ftx.amount_to_precision(symbol,portion/price))
    ftx.create_limit_buy_order(symbol,size,price)
for symbol in highDf['symbol']:
    price=ftx.fetch_ticker(symbol)
    price=float(price['ask'])
    size=float(ftx.amount_to_precision(symbol,portion/price))
    ftx.create_limit_sell_order(symbol,size,price)