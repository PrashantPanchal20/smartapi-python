# package import statement
# import sys
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
from SmartApi import SmartConnect #or from smartapi.smartConnect import SmartConnect
from signals import *
# from talib.abstract import *
# import talib
#import smartapi.smartExceptions(for smartExceptions)
token = "U6MVYLHYB73EO5VYRSZFZOPOG4"
totp = pyotp.TOTP(token).now()
# print(totp)
#create object of call
apikey = "6kF1Q7kE"  #https://smartapi.angelbroking.com/apps
username = "IIRA93449"
pwd = "1336"


obj=SmartConnect(api_key = apikey)
data = obj.generateSession(username, pwd, totp)
print(data)

refreshToken= data['data']['refreshToken']
print(refreshToken)
#fetch the feedtoken
feedToken=obj.getfeedToken()
#fetch User Profile
userProfile= obj.getProfile(refreshToken)
# print(userProfile['data']['exchanges'])
print(userProfile)
def order_place(token, symbol, qty, buy_sell, ordertype, price, variety = 'NORMAL', exch_seg = 'NSE', triggerprice = 0):
    try:
        orderparams = {
            "variety": variety,
            "tradingsymbol": symbol,
            "symboltoken": token,
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
        print("Order placement failed: {}".format(e.message))


# Order book
# orders = obj.orderBook()
# # print(orders)
# trades = obj.tradeBook()
# # print(trades)
# position = obj.position()
# # print(position)
# holding = obj.holding()
# # print(holding)
# LTP = obj.ltpData('NFO',token_info['symbol'], token_info['token'])
# # print(LTP)


from datetime import timedelta
#Historic api == Candel data function= Only for Equity segment
def historical_data(token, symbol, interval = "ONE_MINUTE"):  # ONE_MINUTE , THREE_MINUTE, FIVE_MINUTE, TEN_MINUTE, FIFTEEN_MINUTE
    to_date = datetime.now()
    from_date = to_date - timedelta(days=6)
    from_date_format = from_date.strftime("%Y-%m-%d %H:%M")
    to_date_format = to_date.strftime("%Y-%m-%d %H:%M")
    executed_orders_count = 0

    try:
        historicParam={
        "exchange": "NSE",
        "symboltoken": token,
        "interval": interval,
        "fromdate": from_date_format, 
        "todate": to_date_format
        }
        candel_json = obj.getCandleData(historicParam)
        columns = ['timestamp','Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(candel_json['data'], columns = columns)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['timestamp'] = df['timestamp'].dt.strftime("%Y-%m-%d %H:%M")
        return df
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', None)
        # pd.set_option('display.max_rows', None)
        # print(df)  
    except Exception as e:
        print("Historic Api failed: {}".format(e.message))


def EMA15_cross_BBMiddle(data):
    print(data)
    data['Buy_Signal'] = 'No'  # 1 for Buy

# Generate buy signal when 15 EMA crosses the Bollinger Bands middle line from below
    for i in range(1, len(data)):
        if data['15EMA'].iloc[i-1] <= data['Middle'].iloc[i-1] and data['15EMA'].iloc[i] > data['Middle'].iloc[i]:
            data['Buy_Signal'].iloc[i] = 'Buy'
    print(data)
    latest_candel = df.iloc[-1]
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
            order = order_place(token, symbol, qty, 'BUY', 'MARKET', 0)
            Sell = order_place(token, symbol, qty, 'SELL', 'STOPLOSS_MARKET', 0 , variety = 'STOPLOSS', triggerprice = SL)
            TGT = order_place(token, symbol, qty, 'SELL', 'LIMIT', target)
            print(f'Order Placed SL {SL} TGT {target} QTY {qty} at {datetime.now()}')
        else: 
            print('All Orders Executed')
    else:
        print(f'Order not Placed because Here is no "Buy Signal" at SL {SL} TGT {target} QTY {qty} at {datetime.now()}')

    # df.tail(10)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_rows', None)
    # ema_strategy(df)
    # calculate_bollinger_bands(df)
    # EMA15_cross_BBMiddle(df)
    # print(df)

def run_code():
    while True:
    # Set the desired time frame (e.g., 65 seconds from the start time)
        start = time.time()
        print(start)
        timeFrame = datetime.fromtimestamp(start) + timedelta(seconds=65)
        time_remaining = (timeFrame - datetime.fromtimestamp(start)).total_seconds()
        print("Time Remaining: ", str(timedelta(seconds=time_remaining)))

        # Sleep for the calculated time interval
        time.sleep(time_remaining)
        historical_data(1660, 'ITC-EQ')   #Nifty showing Error. code 65622, ITC=1660
        print(df)
        ema_strategy(df)
        calculate_bollinger_bands(df)
        EMA15_cross_BBMiddle(df)

run_code()

    # print(df['timestamp','Open', 'High', 'Low', 'Close', 'Volumn', 'EMA_20', 'RSI_14', 'ATR_14'])
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', None)
    # pd.set_option('display.max_rows', None)
    # print(df)


    # Assuming df is your pandas DataFrame with OHLC data including the 'Volume' column

# Feature engineering: Creating a simple feature for demonstration
    # df['PriceChange'] = df['Close'].pct_change()
    # df['VolumeChange'] = df['Volumn'].pct_change()
    # df['Target'] = df['PriceChange'].shift(-1)  # Shift target by one day

    # # Drop NaN values
    # df.dropna(inplace=True)

    # # Features and target variable
    # X = df[['PriceChange', 'VolumeChange']]
    # y = df['Target']

    # # Split the data into training and testing sets
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # # Initialize the Decision Tree Regressor
    # regressor = DecisionTreeRegressor()

    # # Train the model
    # regressor.fit(X_train, y_train)

    # # Make predictions on the full dataset
    # df['PredictedChange'] = regressor.predict(X)

    # # Set thresholds for deciding when to buy or sell
    # buy_threshold = 0.005  # Positive change threshold for buy signal
    # sell_threshold = -0.005  # Negative change threshold for sell signal
    # reward_ratio = 2.0  # Risk-reward ratio for the additional buy signal

    # # Generate buy, sell, and reward signals
    # df['BuySignal'] = ((df['PredictedChange'] > buy_threshold) & (df['VolumeChange'] > 0)).astype(int)
    # df['SellSignal'] = ((df['PredictedChange'] < sell_threshold) & (df['VolumeChange'] > 0)).astype(int)
    # df['RewardSignal'] = ((df['PredictedChange'] > buy_threshold * reward_ratio) & (df['VolumeChange'] > 0)).astype(int)

    # # Cumulative signals
    # df['CumulativeBuySignal'] = df['BuySignal'].cumsum()
    # df['CumulativeSellSignal'] = df['SellSignal'].cumsum()
    # df['CumulativeRewardSignal'] = df['RewardSignal'].cumsum()



    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', None)
    # pd.set_option('display.max_rows', None)
    # print(df)
    
# indicator applied


#logout
# try:
#     logout=obj.terminateSession('Your Client Id')
#     print("Logout Successfull")
# except Exception as e:
#     print("Logout failed: {}".format(e.message))


# gtt rule creation
# try:
#     gttCreateParams={
#             "tradingsymbol" : "SBIN-EQ",
#             "symboltoken" : "3045",
#             "exchange" : "NSE", 
#             "producttype" : "MARGIN",
#             "transactiontype" : "BUY",
#             "price" : 100000,
#             "qty" : 10,
#             "disclosedqty": 10,
#             "triggerprice" : 200000,
#             "timeperiod" : 365
#         }
#     rule_id=obj.gttCreateRule(gttCreateParams)
#     print("The GTT rule id is: {}".format(rule_id))
# except Exception as e:
#     print("GTT Rule creation failed: {}".format(e.message))
    
# #gtt rule list
# try:
#     status=["FORALL"] #should be a list
#     page=1
#     count=10
#     lists=obj.gttLists(status,page,count)
# except Exception as e:
#     print("GTT Rule List failed: {}".format(e.message))


# ## WebSocket

# from SmartApi.webSocket import WebSocket

# FEED_TOKEN= feedToken
# CLIENT_CODE="IIRA93449"
# token="mcx_fo|224570&nse_cm|2885&nse_fo|53179&cde_fo|7395" #"nse_cm|2885&nse_cm|1594&nse_cm|11536"
# task="mw" #"mw"|"sfi"|"dp"
# ss = WebSocket(FEED_TOKEN, CLIENT_CODE)

# def on_message(ws,message):
#     print("Ticks: {}".format(message))

# def on_open(ws):
#     print("on open")
#     ss.subscribe(task, token)

# def on_error(ws, error):
#     print("Error")
    
# def on_close(ws):
#     print("close")

# def on_tick(ws, tick):
#     print("Ticks: {}".format(tick))

# def on_connect(ws, response):
#     ws.websocket_connection() # Websocket connection  
#     ws.send_request(token,task) 
    
# def on_close(ws, code, reason):
#     ws.stop()

# # Assign the callbacks.
# ss.on_open = on_open
# ss._on_message = on_message
# ss._on_error = on_error
# ss.on_ticks = on_tick
# ss.on_connect = on_connect
# ss.on_close = on_close

# ss.connect()


