import telebot
import requests
import time

# Вставьте сюда токен от BotFather
TOKEN = 8415401903:AAHV3PRhUFSxS4-1N0nbHi4WPaeCLJ609eU

bot = telebot.TeleBot(TOKEN)

PAIR = "SOLUSDT"
INTERVAL = "15m"
BINANCE_URL = "https://api.binance.com/api/v3/klines"

def get_price():
    try:
        params = {"symbol": PAIR, "interval": INTERVAL, "limit": 1}
        response = requests.get(BINANCE_URL, params=params)
        data = response.json()
        close_price = float(data[0][4])  # последняя цена закрытия
        return close_price
    except Exception as e:
        return f"Ошибка получения цены: {e}"

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "✅ Бот запущен!\nЯ буду показывать цену SOL/USDT (таймфрейм 15м).")

@bot.message_handler(commands=['price'])
def price_message(message):
    price = get_price()
    bot.send_message(message.chat.id, f"💰 Цена SOL/USDT: {price}")

print("Бот запущен...")
bot.polling()
