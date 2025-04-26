from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests

TOKEN = "7731694868:AAGZvbAApn7hG7Xl-NnR1YMIfinKCTgtjvo"
SUPABASE_URL = "https://joiujlddyuspbtmxzwhw.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpvaXVqbGRkeXVzcGJ0bXh6d2h3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU2NTI2NDMsImV4cCI6MjA2MTIyODY0M30.USQ8PFMBIhDyJ-Bt6KvdRy89dc2chFiyFBO-rtVlfmw"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("Привет! Напиши название блюда, и я покажу его ТТК.")

@dp.message_handler()
async def get_ttk(msg: types.Message):
    query = msg.text
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    }
    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/ttk?dish_name=eq.{query}",
        headers=headers
    )
    data = res.json()
    if data:
        item = data[0]
        await msg.answer(f"🔹 {item['dish_name']}\n📎 {item['ttk_url']}\n💬 {item['description']}")
    else:
        await msg.answer("Такого блюда не нашлось 🤷")

executor.start_polling(dp)
