import ccxt
import pandas as pd
from datetime import datetime,timedelta
from datetime import datetime,timedelta
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

def getBestFr(hours_val):
    frLst=[]
    onehago=datetime.now()-timedelta(hours=hours_val)
    onehago=onehago.replace(second=0, microsecond=0, minute=0, hour=onehago.hour)+timedelta(hours=onehago.minute//30)
    onehago=onehago.timestamp()*1000
    for symbol in symbols:
        fr=ftx.fetch_funding_rate_history(symbol,since=onehago,limit=1)
        fr=pd.DataFrame(fr)
        fr['timestamp']=[datetime.fromtimestamp((x/1000)) for x in fr['timestamp']]
        frLst.append(fr)
    frLst=[[x['fundingRate'][0],x['symbol'][0]] for x in frLst]
    frDf=pd.DataFrame(frLst)
    frDf.columns=['fundingRate','symbol']
    lower=frDf.nsmallest(5,'fundingRate')
    higher=frDf.nlargest(5,'fundingRate')
    return(lower,higher)