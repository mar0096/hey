import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation
import time
import numpy as np

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-t", "--tickers", help="tickers")
parser.add_argument("-i", "--interval", help="interval_time")

args = parser.parse_args()

# mpf.__version__

def BR():
    B3 = []
    R3 = []
    B5 = []
    R5 = []

    

    HH = []
    LL = []
    

    for i in df["BR3"]:
        if i>0:
            R3.append(i)
            B3.append(np.nan)
        elif i<0:
            B3.append(i)
            R3.append(np.nan)
        else:
            R3.append(np.nan)
            B3.append(np.nan)

    
    for i in df["CH"]:
        if i>1.5:
            HH.append(i)
        else:
            HH.append(np.nan)
    
    for i in df["CL"]:
        if i<-1.5:
            LL.append(i)
        else:
            LL.append(np.nan)
    
    for i in df["BR5"]:
        if i>0:
            R5.append(i)
            B5.append(np.nan)
        elif i<0:
            B5.append(i)
            R5.append(np.nan)
        else:
            R5.append(np.nan)
            B5.append(np.nan)

    



    return B3,R3,HH,LL,B5,R5

def line():
    lines = []
    days = 5
    
    indMax = np.argmax(df.close)
    indMin = np.argmin(df.close)
    lineDate = [0,99,indMax,indMin]
    for i in range(days,100-days):
        if df.close[i] == max(df.close[i-days:i+days]) or df.close[i] == min(df.close[i-days:i+days]):
            lineDate.append(i)
    
    list(set(lineDate))
    lineDate.sort()
    for i in lineDate:
        lines.append((df.close.index[i],df.close[i]))

    
    
    return lines

df = pd.read_csv('data/'+args.tickers+'_'+args.interval+'m.csv',index_col=0,parse_dates=True, engine='python')

df = df.tail(1000)
B3,R3,HH,LL,B5,R5 = BR()
# lines = line()

apds = [mpf.make_addplot(df['exp12'],color='lime'),
        mpf.make_addplot(df['exp26'],color='c'),
        # mpf.make_addplot(df['histogram'],type='bar',width=0.7,panel=1,
        #                 color='dimgray',alpha=1,secondary_y=False),
        mpf.make_addplot(df['macd'],panel=2,color='fuchsia',secondary_y=True),
        mpf.make_addplot(df['signal'],panel=2,color='b',secondary_y=True),
        # mpf.make_addplot(R3,panel=1,type='scatter',marker='^',markersize=100,color='r'),
        # mpf.make_addplot(B3,panel=1,type='scatter',marker='v',markersize=100,color='black'),
        mpf.make_addplot(df["CH5"],color='black',panel=1),
    ]

s = mpf.make_mpf_style(base_mpf_style='classic',rc={'figure.facecolor':'lightgray'})

fig, axes = mpf.plot(df,type='candle',addplot=apds,figscale=1.7,figratio=(9,6),title=args.tickers+'  '+args.interval+'m',
                     style=s,volume=True,volume_panel=3,panel_ratios=(9,3,3,3),returnfig=True,tight_layout=True)



def animate(ival):
    
    time.sleep(5)

    df = pd.read_csv('data/'+args.tickers+'_'+args.interval+'m.csv',index_col=0,parse_dates=True, engine='python')
    df = df.tail(1000)
    B3,R3,HH,LL,B5,R5 = BR()
    # lines = line()

    apds = [mpf.make_addplot(df['exp12'],color='lime',ax=axes[0]),
            mpf.make_addplot(df['exp26'],color='c',ax=axes[0]),
            # mpf.make_addplot(df['histogram'],type='bar',width=0.7,
            #                  color='dimgray',alpha=1,ax=ax_hisg),
            
            mpf.make_addplot(R3,type='scatter',marker='^',markersize=50,color='r',ax=axes[2]),
            mpf.make_addplot(B3,type='scatter',marker='v',markersize=50,color='black',ax=axes[2]),
            mpf.make_addplot(R5,type='scatter',marker='$5$',markersize=50,color='r',ax=axes[2]),
            mpf.make_addplot(B5,type='scatter',marker='$5$',markersize=50,color='black',ax=axes[2]),
            mpf.make_addplot(HH,type='scatter',marker='$\mid$',markersize=100,color='r',ax=axes[2]),
            mpf.make_addplot(LL,type='scatter',marker='$\mid$',markersize=100,color='black',ax=axes[2]),
            mpf.make_addplot(df["TT"],type='scatter',marker='$T$',markersize=100,color='black',ax=axes[2]),
            mpf.make_addplot(df["B2S"],type='scatter',marker='$Stop$',markersize=200,color='black',ax=axes[2]),
            mpf.make_addplot(df["CH5"],color='black',ax=axes[2]),
            mpf.make_addplot(df["CL5"],color='r',ax=axes[2]),
            mpf.make_addplot((df["CH5"]+df["CL5"])*2,color='green',ax=axes[2]),
            mpf.make_addplot(df["S5"],color='green',ax=axes[4]),
            mpf.make_addplot(df["S10"],color='r',ax=axes[4]),
            # mpf.make_addplot(df['macd'],color='fuchsia',ax=axes[4]),
            # mpf.make_addplot(df['signal'],color='b',ax=axes[4]),
            mpf.make_addplot(df['W25'],type='scatter',marker='$W$',markersize=100,color='blue',ax=axes[2]),
           ]

    for ax in axes:
        ax.clear()

    mpf.plot(df,type='candle',addplot=apds,ax=axes[0],volume=axes[6])

ani = animation.FuncAnimation(fig,animate,interval=100)

mpf.show()

