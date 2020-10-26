import json
import pandas as pd
import numpy as np
import time
import yfinance as yf

def candle(df):
    candleC = []
    candleH = []
    candleL = []
    CC = []
    CH = []
    CL = []
    CH5 = []
    CL5 = []
    TT = []
    

    for i in range(len(df)):
        candleC.append(df["close"][i]-df["open"][i])
        candleH.append(df["high"][i]-max([df["open"][i],df["close"][i]]))
        candleL.append(df["low"][i]-min([df["open"][i],df["close"][i]]))
    candleCA = sum(map(abs,candleC))/len(candleC)
    for i in range(len(df)):
        CC.append(candleC[i]/candleCA)
        CH.append(candleH[i]/candleCA)
        CL.append(candleL[i]/candleCA)
        if i > 5 :
            CH5.append(sum(CH[i-5:i]))
            CL5.append(sum(CL[i-5:i]))
        else:
            CH5.append(np.nan)
            CL5.append(np.nan)
    
    for i in range(len(df)):
        if (CH[i]>2 and CL[i] >-0.3 and CC[i]<0.5) :
            TT.append(CH[i]-(CC[i]-CL[i]))
        elif (CH[i]<0.3 and CL[i] <-2 and CC[i]<0.5):
            TT.append(CL[i]-(CC[i]+CH[i]))
        else:
            TT.append(np.nan)

        
        
    
        
    return candleC,candleH,candleL,candleCA,CC,CH,CL,CH5,CL5,TT

def BR33(df,CC):
    BR3 = [np.nan,np.nan]
    B2S = [np.nan,np.nan]
    BR5 = [np.nan,np.nan,np.nan,np.nan,np.nan]

    for i in range(2,len(df)):
        if (CC[i] > 0 and CC[i-1] > 0 and CC[i-2] > 0 and CC[i]+CC[i-1]+CC[i-2]>1.8)or(CC[i] < 0 and CC[i-1] < 0 and CC[i-2] < 0 and CC[i]+CC[i-1]+CC[i-2]<-1.8):
            BR3.append(CC[i]+CC[i-1]+CC[i-2])
        else:
            BR3.append(np.nan) 
        
        if (CC[i] < 0 and CC[i-1] > 0 and CC[i-2] > 0 and CC[i-1]+CC[i-2] > 1.2 and CC[i]+CC[i-1]+CC[i-2] < -0.5) or (CC[i] > 0 and CC[i-1] < 0 and CC[i-2] < 0 and CC[i-1]+CC[i-2] < -1.2 and CC[i]+CC[i-1]+CC[i-2] > 0.5):
            B2S.append(CC[i])
        else:
            B2S.append(np.nan) 
        if i>4:
            if (CC[i] > 0 and CC[i-1] > 0 and CC[i-2] > 0 and CC[i-3] > 0 and CC[i-4] > 0) or (CC[i] < 0 and CC[i-1] < 0 and CC[i-2] < 0 and CC[i-3] < 0 and CC[i-4] < 0):
                BR5.append((CC[i]+CC[i-1]+CC[i-2]+CC[i-3]+CC[i-4])/3)
            else:
                BR5.append(np.nan)

    return BR3,B2S,BR5

def Wave25(df,CH,CL):
    W25 = []
    for i in range(len(df)):
        if CH[i]>1 and CL[i]<-1:
            W25.append(CH[i] - CL[i])
        else:
            W25.append(np.nan)
    return W25

def Slope(df,candleCA):
    S5 = []
    S10 = []
    Pos = []
    for i in range(len(df)):
        if i>10:
            if -(df["close"][i]-max(df["close"][i-10:i-3])) > (df["close"][i]-min(df["close"][i-10:i-3])):
                S5.append((df["close"][i]-max(df["close"][i-10:i-3]))/candleCA)
            else:
                S5.append((df["close"][i]-min(df["close"][i-10:i-3]))/candleCA)
        else:
            S5.append(np.nan)

        if i>20:
            if -(df["close"][i]-max(df["close"][i-20:i-10])) > (df["close"][i]-min(df["close"][i-20:i-10])):
                S10.append((df["close"][i]-max(df["close"][i-20:i-10]))/candleCA)
            else:
                S10.append((df["close"][i]-min(df["close"][i-20:i-10]))/candleCA)
        else:
            S10.append(np.nan)

        if i>100:
            Pos.append((df["close"][i]-min(df["close"][i-100:i]))/(max(df["close"][i-100:i])-min(df["close"][i-100:i])))
        else:
            Pos.append(np.nan)
        
    return S5,S10,Pos

def getData(tickers,period,interval):
    df = yf.download(tickers=tickers, period=period, interval=interval) 
    df = df.astype('float')
    df.columns = ["open","high","low","close","adjClose","volume"]
    

    exp12     = df['close'].ewm(span=12, adjust=False).mean()
    exp26     = df['close'].ewm(span=26, adjust=False).mean()
    macd      = exp12 - exp26
    signal    = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    candleC,candleH,candleL,candleCA,CC,CH,CL,CH5,CL5,TT = candle(df)
    BR3,B2S,BR5 = BR33(df,CC)
    W25 = Wave25(df,CH,CL)
    S5,S10,Pos = Slope(df,candleCA)



    df["exp12"]     = exp12
    df["exp26"]     = exp26
    df["macd"]      = macd
    df["signal"]    = signal
    df["histogram"] = histogram
    df["BR3"]       = BR3
    df["BR5"]       = BR5
    df["B2S"]       = B2S
    df["CC"]        = CC
    df["CH"]        = CH
    df["CL"]        = CL
    df["CH5"]       = CH5
    df["CL5"]       = CL5
    df["TT"]        = TT
    df["W25"]       = W25
    df["S5"]        = S5
    df["S10"]       = S10
    df["Pos"]       = Pos
    

    


    df.to_csv('Data/'+tickers+"_"+interval+'.csv')

zzz= 0
# df = pd.read_csv('history/GC=F15_history.csv',index_col=0,parse_dates=True)
while 1:
    getData("EURJPY=X","60d","5m")
    getData("EURJPY=X","60d","15m")
    getData("EURJPY=X","60d","60m")
    print(zzz)
    time.sleep(10)
    
    zzz+=1


