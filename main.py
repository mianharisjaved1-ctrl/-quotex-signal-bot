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

bot.send_message(CHAT_ID, "🎯 SNIPER PRO BOT ACTIVATED (HIGH ACCURACY MODE)")

last_price = {}

# -------- RSI STYLE (simple approximation) --------
def rsi_style(old, new):
    if old == 0:
        return 50
    change = new - old
    return 50 + (change * 200)

# -------- SNIPER LOGIC --------
def sniper_signal(symbol, price):
    if symbol not in last_price:
        last_price[symbol] = price
        return None

    old = last_price[symbol]
    last_price[symbol] = price

    momentum = price - old
    rsi = rsi_style(old, price)

    # 🔥 SNIPER CONDITIONS (strict)
    if momentum > 0.0005 and rsi < 70:
        return "📈 STRONG BUY", rsi

    elif momentum < -0.0005 and rsi > 30:
        return "📉 STRONG SELL", rsi

    return None


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


# -------- LOOP --------
while True:
    try:
        for name, symbol in PAIRS.items():

            price = get_price(symbol)

            if price is None:
                continue

            result = sniper_signal(symbol, price)

            # only send sniper signals
            if result:
                signal, rsi = result

                bot.send_message(
                    CHAT_ID,
                    f"🎯 SNIPER PRO SIGNAL\n\n"
                    f"💱 Pair: {name}\n"
                    f"💰 Price: {price}\n"
                    f"📊 RSI: {rsi:.2f}\n"
                    f"⚡ Signal: {signal}\n"
                    f"🔥 HIGH ACCURACY SETUP"
                )

            time.sleep(2)

        time.sleep(60)

    except Exception as e:
        print("SNIPER ERROR:", e)
        time.sleep(5)
