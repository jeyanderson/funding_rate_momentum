import ccxt
import pandas as pd

ftx=ccxt.ftx({
            "apiKey":'apiKey',
            "secret":'secretKey',
            'headers':{
                'FTX-SUBACCOUNT':'subaccountName'
            }
        })
tf='1h'

def get_liquid_symbols():
    markets=ftx.load_markets()
    markets=pd.DataFrame(markets)
    markets=markets.T
    markets=markets[markets['id'].str.contains('-PERP')]
    symbols=markets['id'].to_list()
    volumes=[]
    for symbol in symbols:
        df=ftx.fetch_ticker(symbol)
        volumes.append(df['quoteVolume'])
    volumes=pd.DataFrame(volumes)
    quantile=volumes.quantile(.75)
    quantile=quantile[0]
    volumes=volumes[0].to_list()
    volumes=[v>=quantile for v in volumes]
    markets=markets[volumes]
    return markets['id'].to_list()