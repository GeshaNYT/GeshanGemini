import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Загружаем ключи из настроек Koyeb
TOKEN = os.getenv("BOT_TOKEN")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Настройка модели Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

# Настройка бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Я твой AI-бот на базе Gemini. Напиши мне что угодно!")

# Обработка текстовых сообщений
@dp.message()
async def chat(message: types.Message):
    if not message.text:
        return
    
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        print(f"Ошибка Gemini: {e}")
        await message.answer("Произошла ошибка при обращении к ИИ.")

async def main():
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

# ВАЖНО: подчеркивания должны быть двойными __
if __name__ == "__main__":
    asyncio.run(main())
