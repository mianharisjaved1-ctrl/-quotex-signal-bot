import telebot
import time
import requests
import pandas as pd

TOKEN = "8671909594:AAGzbMdw9SCbk2DP16MabrR_6u4PVc1gjyI"
CHAT_ID = "7036550926"

bot = telebot.TeleBot(TOKEN)

# Forex pairs (real market symbols via free API proxy)
PAIRS = {
    "EURUSD": "EURUSD",
    "GBPUSD": "GBPUSD",
    "USDJPY": "USDJPY",
    "GOLD": "XAUUSD"
}

bot.send_message(CHAT_ID, "🚀 Simple Forex Signal Bot Started")

# -------- GET REAL DATA --------
def get_data(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=50&apikey=demo"
    data = requests.get(url).json()
print("API RESPONSE:", data)
    if "values" not in data:
        return None

    closes = [float(i["close"]) for i in data["values"]]
    closes.reverse()
    return closes

# -------- INDICATORS --------
def ema(data, period):
    return pd.Series(data).ewm(span=period).mean().iloc[-1]

def rsi(data, period=14):
    series = pd.Series(data)
    delta = series.diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs)).iloc[-1]

# -------- SIGNAL ENGINE --------
def get_signal(data):
    short = ema(data, 5)
    long = ema(data, 15)
    rsi_val = rsi(data)

    if short > long and rsi_val < 70:
        return "📈 BUY", rsi_val
    elif short < long and rsi_val > 30:
        return "📉 SELL", rsi_val
    else:
        return "⏸ NO TRADE", rsi_val

# -------- LOOP --------
while True:
    try:
        for name, symbol in PAIRS.items():

            data = get_data(symbol)

            if data is None or len(data) < 20:
                continue

            signal, rsi_val = get_signal(data)

            price = data[-1]

            bot.send_message(
                CHAT_ID,
                f"📊 FOREX SIGNAL\n\n"
                f"💱 Pair: {name}\n"
                f"💰 Price: {price:.4f}\n"
                f"📉 RSI: {rsi_val:.2f}\n"
                f"⚡ Signal: {signal}"
            )

            time.sleep(3)

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
