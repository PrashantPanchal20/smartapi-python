# package import statement
import sys
sys.path.append("C:\Users\panch\Desktop\Prashant\smartapi-python\SmartApi")
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

def gettokenInfo(token_df, exch_seg, instrumenttype, symbol, strike_price, pe_ce ):
    strike_price = strike_price * 100

    if exch_seg == 'NSE':
        eq_df = token_df[(token_df['exch_seg'] == 'NSE') & (token_df['symbol'].str.contains('EQ'))]
        # print(eq_df[eq_df['Name'] == symbol])
        return eq_df[eq_df['Name'] == symbol]
    
    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return token_df[(token_df['exch_seg'] == 'NFO') & (token_df['instrumenttype'] == instrumenttype) & (token_df['name'] == symbol)].sort_values(by=['expiry'])
    
    elif exch_seg == 'NFO' and ((instrumenttype == 'OPTSTK') or (instrumenttype == 'OPTIDX')):
        return token_df[(token_df['exch_seg'] == 'NFO') & (token_df['instrumenttype'] == instrumenttype) & (token_df['name'] == symbol) & (token_df['strike'] == strike_price) & (token_df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])

json_url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
response  = requests.get(json_url)

if response.status_code == 200:
    json_data = response.json()
    token_df = pd.DataFrame.from_dict(json_data)
    token_df['expiry'] = pd.to_datetime(token_df['expiry'])
    token_df = token_df.astype({'strike':float})
    # print(token_df)
else: 
    print(f"Failed to fetch data. Status code: {response.status_code}")
# token_df.to_csv(r'C:\Users\panch\Desktop\Prashant\smartapi-python' + 'angle_token.csv', header=True, index=False) #for save file into csv format
token_info = gettokenInfo(token_df, 'NFO', 'OPTIDX', 'NIFTY', 21400, 'PE').iloc[0]
print(token_info['symbol'], token_info['token'], token_info['lotsize'])
# place order
# try:
#     orderparams = {
#         "variety": "NORMAL",
#         "tradingsymbol": token_info['symbol'],
#         "symboltoken": token_info['token'],
#         "transactiontype": "BUY",
#         "exchange": "NSE",
#         "ordertype": "LIMIT",
#         "producttype": "INTRADAY",
#         "duration": "DAY",
#         "price": "0",
#         "squareoff": "0",
#         "stoploss": "0",
#         "quantity": token_info['lotsize']
#         }
#     orderId=obj.placeOrder(orderparams)
#     print("The order id is: {}".format(orderId))
# except Exception as e:
#     print("Order placement failed: {}".format(e.message))


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


#Historic api == Candel data function= Only for Equity segment
# def historical_data():
#     try:
#         historicParam={
#         "exchange": "NSE",
#         "symboltoken": "3045",
#         "interval": "ONE_MINUTE",
#         "fromdate": "2021-02-08 09:15", 
#         "todate": "2021-02-08 10:30"
#         }
#         return obj.getCandleData(historicParam)
#     except Exception as e:
#         print("Historic Api failed: {}".format(e.message))

#     # print(obj.getCandleData(historicParam))

# res_json = historical_data()
# # print(res_json)
# columns = ['timestamp','Open', 'High', 'Low', 'Close', 'Volumn']
# df = pd.DataFrame(res_json['data'], columns = columns)
# df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601')  #ISO8601  , %y-%m-%dT%H:%M:%S , mixed
# print(df)

from datetime import timedelta
#Historic api == Candel data function= Only for Equity segment
def historical_data(token, interval = "FIFTEEN_MINUTE"):
    to_date = datetime.now()
    from_date = to_date - timedelta(days=3)
    from_date_format = from_date.strftime("%Y-%m-%d %H:%M")
    to_date_format = to_date.strftime("%Y-%m-%d %H:%M")

    try:
        historicParam={
        "exchange": "NSE",
        "symboltoken": token,
        "interval": interval,
        "fromdate": from_date_format, 
        "todate": to_date_format
        }
        candel_json = obj.getCandleData(historicParam)
        columns = ['timestamp','Open', 'High', 'Low', 'Close', 'Volumn']
        df = pd.DataFrame(candel_json['data'], columns = columns)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['timestamp'] = df['timestamp'].dt.strftime("%Y-%m-%d %H:%M")
        return df

    except Exception as e:
        print("Historic Api failed: {}".format(e.message))

#indicator applied
    # df['EMA_20'] = talib.EMA(df.close, timeperiod = 20)
    # df['RSI_14'] = talib.RSI(df.close, timeperiod = 14)
    # df['ATR_20'] = talib.ATR(df.High, df.Low, df.close, timeperiod = 20)

    print(df)

historical_data(1660)   #Nifty showing Error. code 65622, ITC=1660

#indicator applied


# #logout
# try:
#     logout=obj.terminateSession('Your Client Id')
#     print("Logout Successfull")
# except Exception as e:
#     print("Logout failed: {}".format(e.message))


#gtt rule creation
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

# FEED_TOKEN= "your feed token"
# CLIENT_CODE="your client Id"
# token="channel you want the information of" #"nse_cm|2885&nse_cm|1594&nse_cm|11536"
# task="task" #"mw"|"sfi"|"dp"
# ss = WebSocket(FEED_TOKEN, CLIENT_CODE)

# def on_tick(ws, tick):
#     print("Ticks: {}".format(tick))

# def on_connect(ws, response):
#     ws.websocket_connection() # Websocket connection  
#     ws.send_request(token,task) 
    
# def on_close(ws, code, reason):
#     ws.stop()

# # Assign the callbacks.
# ss.on_ticks = on_tick
# ss.on_connect = on_connect
# ss.on_close = on_close

# ss.connect()


