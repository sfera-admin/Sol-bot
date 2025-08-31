import os, time, requests, telebot

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN env var is missing")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

PAIR = "SOLUSDT"
INTERVAL = "15m"
BINANCE_URL = "https://api.binance.com/api/v3/klines"

def latest_close():
    r = requests.get(BINANCE_URL, params={"symbol": PAIR, "interval": INTERVAL, "limit": 1}, timeout=10)
    r.raise_for_status()
    return float(r.json()[0][4])

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "✅ Бот запущен. Команды:\n/price — текущая цена SOL/USDT (15m)")

@bot.message_handler(commands=['price'])
def price(m):
    try:
        p = latest_close()
        bot.reply_to(m, f"💰 SOL/USDT: <b>{p}</b> (15m)")
    except Exception as e:
        bot.reply_to(m, f"⚠️ Ошибка цены: {e}")

if __name__ == "__main__":
    print("Bot polling...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print("Polling error:", e)
            time.sleep(5)
