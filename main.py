import telebot
import time

TOKEN = "8671909594:AAGzbMdw9SCbk2DP16MabrR_6u4PVc1gjyI"
CHAT_ID = "7036550926"

bot = telebot.TeleBot(TOKEN)

while True:
    try:
        bot.send_message(CHAT_ID, "🤖 Bot is working!")
        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(10)
