from datetime import timedelta
from datetime import datetime
import pandas as pd

def historical_data_(obj, token, symbol, interval = "ONE_MINUTE"):  # ONE_MINUTE , THREE_MINUTE, FIVE_MINUTE, TEN_MINUTE, FIFTEEN_MINUTE
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
        print("Historic Api failed: {}".format(e.args[0]))