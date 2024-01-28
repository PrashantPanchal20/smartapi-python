# package import statement
import sys
# sys.path.append("C:\Users\panch\Desktop\Prashant\smartapi-python\SmartApi")
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

import time
import pyotp
import pandas as pd
from datetime import datetime
import requests
import numpy as np
from datetime import timedelta
from SmartApi import SmartConnect #or from smartapi.smartConnect import SmartConnect
from signals import *
from historical_data import *

token = "U6MVYLHYB73EO5VYRSZFZOPOG4"
totp = pyotp.TOTP(token).now()
print(totp)
apikey = "6kF1Q7kE"  #https://smartapi.angelbroking.com/apps
username = "IIRA93449"
pwd = "1336"

symbol_list = ['ITC']  #,'CDSL','IEX'
traded_symbol = []

obj = SmartConnect(api_key = apikey)
data = obj.generateSession(username, pwd, totp)
refreshToken= data['data']['refreshToken']
userProfile= obj.getProfile(refreshToken)

def order_place(symbol_token, symbol, qty, buy_sell, ordertype, price, variety = 'NORMAL', exch_seg = 'NSE', triggerprice = 0):
    try:
        orderparams = {
            "variety": variety,
            "tradingsymbol": symbol,
            "symboltoken": symbol_token,
            "transactiontype": buy_sell,
            "exchange": exch_seg,
            "ordertype": ordertype,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": price,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty
            }

        orderId = obj.placeOrder(orderparams) 
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(e.args[0]))
        


from datetime import timedelta
from datetime import datetime

def EMA15_cross_BBMiddle(data, symbol, symbol_token):
    executed_orders_count = 0
    data['Buy_Signal'] = 'No'  # 1 for Buy

# Generate buy signal when 15 EMA crosses the Bollinger Bands middle line from below
    # for i in range(1, len(data)):
    #     if data['15EMA'].iloc[i-1] <= data['Middle'].iloc[i-1] and data['15EMA'].iloc[i] > data['Middle'].iloc[i]:
    #         data['Buy_Signal'].iloc[i] = 'Buy'
    # print(data.tail(20))
    # for i in range(1, len(data)):
    #     if (all(data['Close'].iloc[-4:] > data['15EMA'].iloc[-4:]) and all(data['15EMA'].iloc[-4:] > data['15EMA'].shift(-1).iloc[-4:])):
    #         data['Buy_Signal'].iloc[i] = 'Buy'
    #     else:
    #         data['Buy_Signal'].iloc[i] = 'No'
    # print(data)

    # for i, row in df.iterrows():
    list_EMA_Values = [] 
    list_close_Values = []
    list_close_signal = []
    list_EMA_Values.clear()
    list_close_Values.clear()
    list_EMA_Values.clear()
    for i in range(1, len(data)):
        list_EMA_Values.append(data['15EMA'].iloc[i])
        list_close_Values.append(data['Close'].iloc[i])
        list_close_signal.append(data['Buy_Signal'].iloc[i])
        
        # print("Index is = ", i ,list_close_signal)
        if(i > 6): 
            last_4_values_ema = list_EMA_Values[-5:-1]
            last_4_values_close = list_close_Values[-5:-1]
            last_4_values_signal = list_close_signal[-7:]
            # print(i, last_4_values_ema, "/////", last_4_values_close, last_4_values_signal)

            if (last_4_values_ema[0] < last_4_values_ema[1] < last_4_values_ema[2] < last_4_values_ema[3]):
                if (last_4_values_close[0] >= last_4_values_ema[0] and last_4_values_close[1] >= last_4_values_ema[1] and last_4_values_close[2] >= last_4_values_ema[2] and last_4_values_close[3] >= last_4_values_ema[3]):
                    if (last_4_values_signal[0] == 'Buy' or last_4_values_signal[1] == 'Buy' or last_4_values_signal[2] == 'Buy' or last_4_values_signal[3] == 'Buy' or last_4_values_signal[4] == 'Buy' or last_4_values_signal[5] == 'Buy'):
                        pass
                    else:
                        data.at[i, 'Buy_Signal'] = 'Buy'
                        list_close_signal.append('Buy')
                        # print("111", list_close_signal)
                else:
                    pass
            else:
                pass
        else:
            pass
            print("I is less than 10 here.")

    print(data)

    latest_candel = data.iloc[-1]   #change -1 in live market
    print(latest_candel)
    LTP = latest_candel['Close']
    # SL = LTP - 2*latest_candel['ATR_20']
    # target = LTP + 5*latest_candel['ATR_20']
    SL = LTP - 1
    target = LTP + 2
    qty = 1
    # return data
    if(latest_candel['Buy_Signal'] == 'Buy'):
        executed_orders_count += 1
        if(executed_orders_count < 4):
        # get last data
            order = order_place(symbol_token, symbol, qty, 'BUY', 'MARKET', 0)
            Sell = order_place(symbol_token, symbol, qty, 'SELL', 'STOPLOSS_MARKET', 0 , variety = 'STOPLOSS', triggerprice = SL)
            TGT = order_place(symbol_token, symbol, qty, 'SELL', 'LIMIT', target)
            print(f'Order Placed SL {SL} TGT {target} QTY {qty} at {datetime.now()}')
            
        else: 
            pass
            print('All Orders Executed')
    else:
        pass
        print(f'Order not Placed because Here is no "Buy Signal" at SL {SL} TGT {target} QTY {qty} at {datetime.now()}')

def run_code():
    while True:
    # Set the desired time frame (e.g., 65 seconds from the start time)
        start = time.time()
        print(start)
        timeFrame = datetime.fromtimestamp(start) + timedelta(seconds=65)
        time_remaining = (timeFrame - datetime.fromtimestamp(start)).total_seconds()
        print("Time Remaining: ", str(timedelta(seconds=time_remaining)))

        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_rows', None)
        df = historical_data_(obj, 1660)   #Nifty showing Error. code 65622, ITC=1660
        # print(df.tail(20))
        ema_strategy(df)
        calculate_bollinger_bands(df)
        EMA15_cross_BBMiddle(df, 'ITC', 1660)   
        time.sleep(time_remaining)

run_code()

