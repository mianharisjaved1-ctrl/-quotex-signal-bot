import time
import telebot
import random

TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

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
