# package import statement
# import sys
# sys.path.append("C:\Users\panch\Desktop\Prashant\smartapi-python\SmartApi")
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import ta
import time
import pyotp
import pandas as pd
from datetime import datetime
import requests
import numpy as np
from SmartApi import SmartConnect #or from smartapi.smartConnect import SmartConnect
# from talib.abstract import *
# import talib
#import smartapi.smartExceptions(for smartExceptions)
token = "U6MVYLHYB73EO5VYRSZFZOPOG4"
totp = pyotp.TOTP(token).now()
# print(totp)
#create object of call
apikey = "1ZRvKQlF"
username = "IIRA93449"
pwd = "1336"


obj=SmartConnect(api_key = apikey)
data = obj.generateSession(username, pwd, totp)
# print(data)
refreshToken= data['data']['refreshToken']
# print(refreshToken)
#fetch the feedtoken
feedToken=obj.getfeedToken()
#fetch User Profile
userProfile= obj.getProfile(refreshToken)
# print(userProfile['data']['exchanges'])
# print(userProfile)

# def gettokenInfo(token_df, symbol, exch_seg = 'NSE', instrumenttype = 'OPTIDX', strike_price = '', pe_ce = 'CE' ):
#     strike_price = strike_price * 100

#     if exch_seg == 'NSE':
#         eq_df = token_df[(token_df['exch_seg'] == 'NSE') & (token_df['symbol'].str.contains('EQ'))]
#         # print(eq_df[eq_df['Name'] == symbol])
#         return eq_df[eq_df['Name'] == symbol]
    
#     elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
#         return token_df[(token_df['exch_seg'] == 'NFO') & (token_df['instrumenttype'] == instrumenttype) & (token_df['name'] == symbol)].sort_values(by=['expiry'])
    
#     elif exch_seg == 'NFO' and ((instrumenttype == 'OPTSTK') or (instrumenttype == 'OPTIDX')):
#         return token_df[(token_df['exch_seg'] == 'NFO') & (token_df['instrumenttype'] == instrumenttype) & (token_df['name'] == symbol) & (token_df['strike'] == strike_price) & (token_df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])

# json_url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
# try:
#     response  = requests.get(json_url, verify=True)
#     response.raise_for_status()  # Raise an HTTPError for bad responses
#     # print(response.text)
# except requests.exceptions.RequestException as e:
#     print(f"Error: {e}")


# if response.status_code == 200:
#     json_data = response.json()
#     token_df = pd.DataFrame.from_dict(json_data)
#     token_df['expiry'] = pd.to_datetime(token_df['expiry'])
#     token_df = token_df.astype({'strike':float})
#     # print(token_df)
# else: 
#     print(f"Failed to fetch data. Status code: {response.status_code}")
# # token_df.to_csv(r'C:\Users\panch\Desktop\Prashant\smartapi-python' + 'angle_token.csv', header=True, index=False) #for save file into csv format
# # token_info = gettokenInfo(token_df, 'NFO', 'OPTIDX', 'NIFTY', 21400, 'PE').iloc[0]
# token_info = gettokenInfo(token_df,'ITC').iloc[0]
# print(token_info['symbol'], token_info['token'], token_info['lotsize'])
# # place order

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
        # return df
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.width', None)
        # pd.set_option('display.max_rows', None)
        # print(df)  
        

    except Exception as e:
        print("Historic Api failed: {}".format(e.message))
    
    def RSI(df):
        rsi_period = 14
        # Calculate daily price changes
        delta = df['Close'].diff(1)
        # Calculate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        # Calculate average gains and losses over the specified period
        average_gain = gain.rolling(window=rsi_period, min_periods=1).mean()
        average_loss = loss.rolling(window=rsi_period, min_periods=1).mean()
        # Calculate relative strength (RS)
        rs = average_gain / average_loss
        # Calculate the RSI
        df['RSI_14'] = 100 - (100 / (1 + rs))

        # Replace 'high', 'low', and 'close' with the actual column names in your DataFrame
        high_prices = df['High']
        low_prices = df['Low']
        close_prices = df['Close']

        # Replace 'your_period' with the desired period for ATR calculation
        # For example, a common period is 14 for a 14-day ATR
        atr_period = 20

        # Calculate True Range (TR)
        tr1 = high_prices - low_prices
        tr2 = abs(high_prices - close_prices.shift())
        tr3 = abs(low_prices - close_prices.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        # Calculate ATR using the rolling mean
        df['ATR_20'] = tr.rolling(window=atr_period).mean()

#Stratagy on the basis of EMA, RSI and ATR
    # df['Cross_Up'] = df['Cross_Down'] = df['RSI_Up'] = 0
    # df['Buy/Sell'] = 'No'
    # df = df.round(decimals = 2)

    # for i  in range(20, len(df)):
    #     if df['Close'][i-1] <= df['EMA_20'][i-1] and df['Close'][i] > df['EMA_20'][i]:
    #         df['Cross_Up'][i] = 1
    #     if df['Close'][i-1] >= df['EMA_20'][i-1] and df['Close'][i] < df['EMA_20'][i]:
    #         df['Cross_Down'][i] = 1
    #     if df['RSI_14'][i] > 38: #50
    #         df['RSI_Up'][i] = 1
    
    #     if df['Cross_Up'][i] == 1 and df['RSI_Up'][i] ==1 :
    #         df['Buy/Sell'][i] = 'Buy'
    
#EMA based statigy applyied
    def calculate_bollinger_bands(data, window=20, num_std_dev=1.5):
        data['PriceChange'] = data['Close'].pct_change()
        
        # Drop NaN values
        data.dropna(inplace=True)
        
        # Calculate Bollinger Bands
        data['Middle'] = data['Close'].rolling(window=window).mean()
        data['bb_upper'] = ta.volatility.bollinger_hband(data['Close'], window=window, window_dev=num_std_dev)
        
        return data

    # Create a column for sell signals
    # df['SellSignal'] = 'No'
    # Identify candles closing from above to below the upper Bollinger Band
    # sell_condition = (df['Close'] > df['bb_upper'].shift(1)) & (df['Close'] < df['bb_upper'])
    # Apply sell signal to the confirmation candle
    # df.loc[sell_condition, 'SellSignal'] = 'Sell'


    # Display the DataFrame with predictions
    # print(df[['timestamp', 'Close', 'PriceChange', 'PredictedChange']])
    def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
        data['12EMA'] = data['Close'].ewm(span=fast_period, adjust=False).mean()
        data['26EMA'] = data['Close'].ewm(span=slow_period, adjust=False).mean()
        
        data['MACD'] = data['12EMA'] - data['26EMA']
        
        data['Signal_Line'] = data['MACD'].ewm(span=signal_period, adjust=False).mean()
        # data['EMA_slope'] = np.polyfit(data.index, df['EMA_15'], 1)
        return data

    def ema_strategy(data):
        data['15EMA'] = data['Close'].ewm(span=15, adjust=False).mean()
        data['30EMA'] = data['Close'].ewm(span=30, adjust=False).mean()
        
        # data = calculate_macd(data)
        # data['Volume_MA'] = data['Volume'].rolling(window=20).mean()54rt         
        # data['Signal'] = 0  # 1 for Buy, -1 for Sell
        
        # # Entry condition
        # data.loc[(data['15EMA'] > data['30EMA']) & (data['MACD'] > data['Signal_Line']) & (data['Volume'] > data['Volume_MA']), 'Signal'] = 1
        
        # # Exit condition
        # data.loc[data['Signal'].shift(1) == 1, 'Target'] = data['Close'] * 1.04  # 4:1 risk-reward ratio
        return data

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
    ema_strategy(df)
    calculate_bollinger_bands(df)
    EMA15_cross_BBMiddle(df)
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


