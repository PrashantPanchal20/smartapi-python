def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    data['12EMA'] = data['Close'].ewm(span=fast_period, adjust=False).mean()
    data['26EMA'] = data['Close'].ewm(span=slow_period, adjust=False).mean()
    
    data['MACD'] = data['12EMA'] - data['26EMA']
    
    data['Signal_Line'] = data['MACD'].ewm(span=signal_period, adjust=False).mean()
    # data['EMA_slope'] = np.polyfit(data.index, df['EMA_15'], 1)
    return data

import ta
def calculate_bollinger_bands(data, window=20, num_std_dev=1.5):
    data['PriceChange'] = data['Close'].pct_change()
    
    # Drop NaN values
    data.dropna(inplace=True)
    
    # Calculate Bollinger Bands
    data['Middle'] = data['Close'].rolling(window=window).mean()
    data['bb_upper'] = ta.volatility.bollinger_hband(data['Close'], window=window, window_dev=num_std_dev)
    
    return data

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