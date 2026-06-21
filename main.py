import telebot
import time
import random

TOKEN = "8671909594:AAGzbMdw9SCbk2DP16MabrR_6u4PVc1gjyI"
CHAT_ID = "7036550926"

bot = telebot.TeleBot(TOKEN)

# simple EMA simulation
def ema(values, period):
    return sum(values[-period:]) / period

def rsi(values, period=14):
    gains = []
    losses = []

    for i in range(1, len(values)):
        diff = values[i] - values[i-1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

prices = [random.uniform(1, 100) for _ in range(50)]

bot.send_message(CHAT_ID, "🤖 Advanced Signal Bot Started!")

while True:
    try:
        # simulate new price
        new_price = prices[-1] + random.uniform(-2, 2)
        prices.append(new_price)

        short_ema = ema(prices, 5)
        long_ema = ema(prices, 15)
        rsi_value = rsi(prices)

        signal = "NO TRADE ⏸"

        if short_ema > long_ema and rsi_value < 70:
            signal = "📈 BUY"
        elif short_ema < long_ema and rsi_value > 30:
            signal = "📉 SELL"

        bot.send_message(
            CHAT_ID,
            f"📊 Signal Update\n"
            f"Price: {new_price:.2f}\n"
            f"RSI: {rsi_value:.2f}\n"
            f"Signal: {signal}"
        )

        time.sleep(60)

    except Exception as e:
        print(e)
        time.sleep(10)
