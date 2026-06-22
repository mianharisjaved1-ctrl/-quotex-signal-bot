import telebot
import time
import requests

TOKEN = "8671909594:AAGzbMdw9SCbk2DP16MabrR_6u4PVc1gjyI"
CHAT_ID = "7036550926"

bot = telebot.TeleBot(TOKEN)

PAIRS = {
    "EURUSD": "EUR/USD",
    "GBPUSD": "GBP/USD",
    "USDJPY": "USD/JPY",
    "GOLD": "XAU/USD"
}

bot.send_message(CHAT_ID, "🚀 Light Forex Bot Started (Stable Version)")

# -------- GET PRICE --------
def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey=demo"
        data = requests.get(url, timeout=10).json()

        if "price" not in data:
            return None

        return float(data["price"])

    except:
        return None


# -------- SIGNAL LOGIC --------
last_prices = {}

def signal_logic(symbol, price):
    if symbol not in last_prices:
        last_prices[symbol] = price
        return "⏸ NO TRADE"

    old = last_prices[symbol]
    last_prices[symbol] = price

    if price > old:
        return "📈 BUY"
    elif price < old:
        return "📉 SELL"
    else:
        return "⏸ NO TRADE"


# -------- LOOP --------
while True:
    try:
        for name, symbol in PAIRS.items():

            price = get_price(symbol)

            if price is None:
                continue   # ❗ no spam message

            signal = signal_logic(symbol, price)

            bot.send_message(
                CHAT_ID,
                f"📊 FOREX LIGHT SIGNAL\n\n"
                f"💱 Pair: {name}\n"
                f"💰 Price: {price}\n"
                f"⚡ Signal: {signal}"
            )

            time.sleep(2)

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
