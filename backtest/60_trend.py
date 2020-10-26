import json
import pandas as pd
import numpy as np
import time
import yfinance as yf
import mplfinance as mpf
import matplotlib.animation as animation
from pandas import Timestamp

#       GC=F
#       ^GDAXI
#       ^FCHI
#       ^FTSE
holiday = []
end_date = ["2020-07-31","2020-08-07","2020-08-14","2020-08-21","2020-08-28","2020-09-04","2020-09-11","2020-09-18","2020-09-25","2020-10-02","2020-10-09","2020-10-16","2020-10-23"]
###### Gold #######
# tickers = "GC=F"
# interval = "60"
# fee_rate = 0.000235
# end_time = ["15:00:00-04:00","16:00:00-04:00"]

####################  Indices  #################

###### GER30 #######
# tickers = "^GDAXI"
# interval = "60"
# fee_rate = 0.000158
# end_time = ["16:00:00+02:00","17:00:00+02:00"]
# end_time = ["17:00:00+02:00","17:15:00+02:00"]

# ##### FRA40 #######
# tickers = "^FCHI"
# interval = "60"
# fee_rate = 0.000204
# end_time = ["16:00:00+02:00","17:00:00+02:00"]
# end_time = ["17:00:00+02:00","17:15:00+02:00"]

###### UK100 #######
# tickers = "^FTSE"
# interval = "60"
# fee_rate = 0.000255
# end_time = ["15:00:00+01:00","16:00:00+01:00"]

###### HK50  #######
# tickers = "^HSI"
# interval = "60"
# fee_rate = 0.00028
# end_time = ["14:30:00+08:00","15:30:00+08:00"]

###### SPX500 #######
# tickers = "^SPX"
# interval = "60"
# fee_rate = 0.000201
# end_time = ["14:30:00-04:00","15:30:00-04:00"]

###### NSDQ100 #######
# tickers = "^NDX"
# interval = "60"
# fee_rate = 0.000205
# end_time = ["14:30:00-04:00","15:30:00-04:00"]

###### DJ30 #######
tickers = "^DJI"
interval = "60"
fee_rate = 0.000210
end_time = ["14:30:00-04:00","15:30:00-04:00"]


####################  Currency  #################
# tickers = "EURUSD=X"
# interval = "60"
# fee_rate = 0.000084
# end_time = ["21:00:00+01:00","22:00:00+01:00"]

# tickers = "GBPUSD=X"
# interval = "60"
# fee_rate = 0.000130
# end_time = ["21:00:00+01:00","22:00:00+01:00"]

# tickers = "USDCAD=X"
# interval = "60"
# fee_rate = 0.000106
# end_time = ["21:00:00+01:00","22:00:00+01:00"]

# tickers = "USDJPY=X"
# interval = "60"
# fee_rate = 0.000095
# end_time = ["21:00:00+01:00","22:00:00+01:00"]

# tickers = "USDCHF=X"
# interval = "60"
# fee_rate = 0.000177
# end_time = ["21:00:00+01:00","22:00:00+01:00"]

# tickers = "AUDUSD=X"
# interval = "60"
# fee_rate = 0.000154
# end_time = ["21:00:00+01:00","22:00:00+01:00"]

# tickers = "EURGBP=X"
# interval = "60"
# fee_rate = 0.000142
# end_time = ["21:00:00+01:00","22:00:00+01:00"]

# tickers = "EURJPY=X"
# interval = "60"
# fee_rate = 0.000153
# end_time = ["21:00:00+01:00","22:00:00+01:00"]



for i in end_date:
    for a in end_time:
        zzz = i +" "+ a
        holiday.append(Timestamp(zzz))



money = 50
lever = 20
stop_lose = 0.5

print("     ",tickers,"     ",interval,"     ",fee_rate,"    ",money,"     ",lever)

df = pd.read_csv('history/'+tickers+'_'+interval+'m.csv',index_col=0,parse_dates=True, engine='python')

Trade = {}
buy = []
buy_close = []
sell = []
sell_close = []
buy_sell = []
buy_sell_close = []
profit_buy = []
profit_sell = []
profit_buy_sell = []
per_low_buy = []
per_high_sell = []

per_MDD_buy = []
per_MDD_sell = []

low = 0
high = 0

stop_buy = False
stop_sell = False

trade = False
BUY = None


#########################################################
for i in range(len(df)):

    if trade:
        if df["low"][i] < low:
            low = df["low"][i]
        if df["high"][i] > high:
            high = df["high"][i]

        if BUY:
            # if df["S5"][i] < 1 or i == len(df)-1 or ((buy[-1]-low)/buy[-1])*lever > stop_lose or df.index[i] in holiday:
            if df["CH5"][i]+df["CL5"][i] > -1 or i == len(df)-1 or ((buy[-1]-low)/buy[-1])*lever > stop_lose or df.index[i] in holiday:
                if ((buy[-1]-low)/buy[-1])*lever > stop_lose:
                    low = (stop_lose/lever*buy[-1])+buy[-1]
                    stop_buy = True
                    buy_close.append(low)
                    
                else:
                    buy_close.append(df["close"][i])
                    buy_sell_close.append(df["close"][i])


                per_low_buy.append(low)
                
                trade = False
                BUY = None
                Trade[df.close.index[i]] = [2,len(buy_close)]
                

        else:
            # if df["S5"][i] > -1 or i == len(df)-1 or ((high - sell[-1])/sell[-1])*lever > stop_lose or df.index[i] in holiday:
            if df["CH5"][i]+df["CL5"][i] < 1 or i == len(df)-1 or ((high - sell[-1])/sell[-1])*lever > stop_lose or df.index[i] in holiday:
                
                if ((high - sell[-1])/sell[-1])*lever > stop_lose:
                    high = (stop_lose/lever*sell[-1])+sell[-1]
                    stop_sell = True
                    sell_close.append(high)
                    
                else:
                    sell_close.append(df["close"][i])
                    buy_sell_close.append(df["close"][i])

                
                per_high_sell.append(high)
                
                trade = False
                BUY = None
                Trade[df.close.index[i]] = [4,len(sell_close)]
                
        

    else:
        if i != len(df)-1 and  df.index[i] not in holiday:
            # if df["S10"][i] > 1 and df["S5"][i] < 1 and stop_buy == False:
            # if df["S5"][i] > 1 :
            if df["CH5"][i]+df["CL5"][i] < -1:
                BUY = True
                buy.append(df["close"][i])
                
                trade = True
                low = df["low"][i]
                Trade[df.close.index[i]] = [1,len(buy)]
                stop_sell = False

            # elif df["S10"][i] < -1 and df["S5"][i] > -1 and stop_sell == False:
            # elif df["S5"][i] < -1 :
            elif df["CH5"][i]+df["CL5"][i] > 1:
                BUY = False
                sell.append(df["close"][i])
                
                trade = True
                high = df["high"][i]
                Trade[df.close.index[i]] = [3,len(sell)]
                stop_buy = False

################################## analysis result  #################################

times_buy = len(buy)
times_sell = len(sell)
# print(len(buy),len(buy_close))
# print(len(sell),len(sell_close))

for i in range(times_buy):
    profit_buy.append(((buy_close[i]-buy[i])/buy[i])*money*lever)
for i in range(times_sell):
    profit_sell.append(((sell_close[i]-sell[i])/sell[i])*-money*lever)


buy_0 = 0
sell_0 = 0
for i,e in enumerate(Trade):
    if Trade[e][0] == 1:
        profit_buy_sell.append(profit_buy[buy_0])
        buy_0 += 1
    elif Trade[e][0] == 3:
        profit_buy_sell.append(profit_sell[sell_0])
        sell_0 += 1

# print(profit_buy_sell)


for i in range(times_buy):
    per_MDD_buy.append((buy[i]-per_low_buy[i])/buy[i]*money*lever)
for i in range(times_sell):
    per_MDD_sell.append((per_high_sell[i]-sell[i])/sell[i]*money*lever)

fee_buy = times_buy*fee_rate*money*lever
fee_sell = times_sell*fee_rate*money*lever
# print(per_high_sell)
# print(per_MDD_sell)

buy_win = list(filter(lambda x: (x >= 0), profit_buy))
buy_lose = list(filter(lambda x: (x < 0), profit_buy))
sell_win = list(filter(lambda x: (x >= 0), profit_sell))
sell_lose = list(filter(lambda x: (x < 0), profit_sell))
# print(buy_win,sell_win)


win_ratio_buy = round(len(buy_win)/times_buy,3) 
win_ratio_sell = round(len(sell_win)/times_sell,3)
win_ratio_all = round((len(buy_win)+len(sell_win))/(times_buy+times_sell),3)

avg_win = (sum(buy_win)+sum(sell_win))/(len(buy_win)+len(sell_win))
avg_loss = (sum(buy_lose)+sum(sell_lose))/(len(buy_lose)+len(sell_lose))
avg_amount = (((sum(buy_win)+sum(sell_win))-(sum(buy_lose)+sum(sell_lose)))/(times_buy+times_sell))


####### compound interest ########
profit_all_percent = []
compound = [float(money)]

for i in profit_buy_sell:
    profit_all_percent.append(i/money)

# print(profit_all_percent)

for i in range(len(profit_all_percent)):
    compound.append(compound[-1]*(1+profit_all_percent[i]))

############### compound  #######################
# print(compound)

print("profit buy        ",round(sum(profit_buy),3))
print("profit sell       ",round(sum(profit_sell),3))
print("profit all        ",round(sum(profit_buy)+sum(profit_sell),3))
print(" ")

print("avg win           ",round(avg_win,3))
print("avg loss          ",round(avg_loss,3))
print("avg amount        ",round(avg_amount,3))
print("Profit Factor     ",round(-avg_win/avg_loss,3))
print(" ")

print("times buy         ",times_buy)
print("times sell        ",times_sell)
print("times all         ",times_buy+times_sell)
print(" ")

print("win ratio buy     ",win_ratio_buy )
print("win ratio sell    ",win_ratio_sell  )
print("win ratio all     ",win_ratio_all)
print(" ")

print("fee buy           ",round(fee_buy,3))
print("fee sell          ",round(fee_sell,3))
print("fee all           ",round(fee_buy+fee_sell,3))
print(" ")

print("net profit buy    ",round(sum(profit_buy)-fee_buy,3))
print("net profit sell   ",round(sum(profit_sell)-fee_sell,3))
print("net profit all    ",round(sum(profit_buy)+sum(profit_sell)-(fee_buy+fee_sell),3))
print("P/A               ",round((sum(profit_buy)+sum(profit_sell)-(fee_buy+fee_sell))/avg_amount,3))
print(" ")

print("highest MDD buy   ",round(max(per_MDD_buy),3))
print("highest MDD sell  ",round(max(per_MDD_sell),3))
print("highest MDD all   ",round(max(max(per_MDD_buy),max(per_MDD_sell)),3))
print(" ")

print("avg MDD buy       ",round(sum(per_MDD_buy)/times_buy,3))
print("avg MDD sell      ",round(sum(per_MDD_sell)/times_sell,3))



###################### draw plot ##################################

lines = []
tlines = []
tlines_color = []

for i in Trade:
    
    lines.append(i)
    if Trade[i][0] == 1:
        tlines_color.append("green")
    elif Trade[i][0] == 3:
        tlines_color.append("r")
    



# print(lines)

for i in range(len(lines)):
    if i%2 == 1:
        tlines.append((lines[i-1],lines[i]))




apds = [mpf.make_addplot(df["S5"],color='green',panel=1),
            mpf.make_addplot(df["S10"],color='r',panel=1),
            mpf.make_addplot((df["CH5"]+df["CL5"]),color='green',panel=2),
    ]

s = mpf.make_mpf_style(base_mpf_style='classic',rc={'figure.facecolor':'lightgray'})

fig, axes = mpf.plot(df,type='candle',figscale=1.7,figratio=(9,6),title=tickers+'  '+interval+'m',addplot=apds,
                     style=s,volume=False,tight_layout=True,tlines=[dict(tlines=tlines,tline_use="close",colors = tlines_color)])

