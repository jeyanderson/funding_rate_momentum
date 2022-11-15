import ccxt
import pandas as pd
from datetime import datetime
from getLiquidPairs import getLiquidSymbols

ftx=ccxt.ftx({
            "apiKey":'apiKey',
            "secret":'secretKey',
            'headers':{
                'FTX-SUBACCOUNT':'subaccountName'
            }
        })
tf='1h'
symbols=getLiquidSymbols()

def getBestFr():
    frLst=[]
    for symbol in symbols:
        fr=ftx.fetch_funding_rate(symbol)
        fr=pd.DataFrame(fr)
        fr['timestamp']=[datetime.fromtimestamp((x/1000)) for x in fr['timestamp']]
        frLst.append(fr)
    frLst=[[x['fundingRate'][0],x['symbol'][0]] for x in frLst]
    frDf=pd.DataFrame(frLst)
    frDf.columns=['fundingRate','symbol']
    lower=frDf.nsmallest(5,'fundingRate')
    higher=frDf.nlargest(5,'fundingRate')
    return(lower,higher)