import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Берем ключи из переменных среды Koyeb
TOKEN = os.getenv("BOT_TOKEN")
genai.configure(api_key=os.getenv("AIzaSyC8zDYK6Ax0zvf3JYAae7I_Zl-YluqU_Xo"))

model = genai.GenerativeModel('gemini-1.5-flash')
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Я бесплатный бот на Gemini.")

@dp.message()
async def chat(message: types.Message):
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception:
        await message.answer("Произошла ошибка запроса.")

async def main():
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
