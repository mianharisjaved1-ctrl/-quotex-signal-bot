import telebot
import time
import requests
import pandas as pd
import numpy as np

TOKEN = "8671909594:AAGzbMdw9SCbk2DP16MabrR_6u4PVc1gjyI"
CHAT_ID = "7036550926"

bot = telebot.TeleBot(TOKEN)

# Forex symbols (Binance proxy / CFD style representation)
SYMBOLS = {
    "EURUSD": "EURUSDT",
    "GBPUSD": "GBPUSDT",
    "GOLD": "XAUUSDT",
    "USDJPY": "USDJPY"
}

bot.send_message(CHAT_ID, "🚀 Forex Pro Signal Bot Started")

# ---------------- DATA ----------------
def get_data(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=60"
    data = requests.get(url).json()
    closes = np.array([float(i[4]) for i in data])
    return closes

# ---------------- INDICATORS ----------------
def ema(data, period):
    return pd.Series(data).ewm(span=period).mean().iloc[-1]

def rsi(data, period=14):
    series = pd.Series(data)
    delta = series.diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs)).iloc[-1]

def volatility(data):
    return np.std(data)

# ---------------- SCORING ----------------
def signal_engine(short_ema, long_ema, rsi_val, vol):
    score = 0

    # trend
    if short_ema > long_ema:
        score += 1
    else:
        score -= 1

    # RSI zones
    if rsi_val < 30:
        score += 2
    elif rsi_val > 70:
        score -= 2

    # volatility filter
    if vol > 2.0:
        score -= 1

    return score

# ---------------- MAIN LOOP ----------------
while True:
    try:
        for name, symbol in SYMBOLS.items():

            prices = get_data(symbol)

            short_ema = ema(prices, 5)
            long_ema = ema(prices, 15)
            rsi_val = rsi(prices)
            vol = volatility(prices)

            score = signal_engine(short_ema, long_ema, rsi_val, vol)

            confidence = min(100, max(0, (abs(score) / 4) * 100))

            if score >= 3:
                signal = "🔥 STRONG BUY"
            elif score <= -3:
                signal = "🔥 STRONG SELL"
            else:
                signal = "⏸ NO TRADE"

            if confidence >= 65:
                bot.send_message(
                    CHAT_ID,
                    f"📊 FOREX PRO SIGNAL\n\n"
                    f"💱 Pair: {name}\n"
                    f"💰 Price: {prices[-1]:.4f}\n"
                    f"📉 RSI: {rsi_val:.2f}\n"
                    f"📊 Score: {score}\n"
                    f"🎯 Confidence: {confidence:.0f}%\n"
                    f"⚡ Signal: {signal}"
                )

            time.sleep(3)

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
