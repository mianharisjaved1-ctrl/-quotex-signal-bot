import time
import telebot
import random

TOKEN ="8671909594:AAETOOdgQ8XfW9UiAUpIUR5RFjIFpi97c-w"
CHAT_ID ="7036550926"

bot = telebot.TeleBot(TOKEN)

def signal():
    rsi = random.randint(30, 70)
    trend = random.choice(["up", "down"])

    if trend == "up" and rsi > 55:
        return "📈 BUY"
    elif trend == "down" and rsi < 45:
        return "📉 SELL"
    else:
        return "⏸ NO TRADE"

while True:
    msg = signal()
    bot.send_message(CHAT_ID, f"Quotex Signal:\n{msg}")
    time.sleep(60)
