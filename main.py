import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Эти данные мы указали в настройках Koyeb (Environment Variables)
TOKEN = os.getenv("BOT_TOKEN")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Настройка нейросети Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

# Настройка бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Реакция на команду /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Я твой AI-бот. Напиши мне что-нибудь, и я отвечу с помощью Gemini!")

# Обработка всех остальных сообщений
@dp.message()
async def chat(message: types.Message):
    if not message.text:
        return
    
    try:
        # Отправляем текст пользователя в Gemini
        response = model.generate_content(message.text)
        # Отправляем ответ нейросети обратно пользователю
        await message.answer(response.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("Произошла ошибка. Проверь API ключи в настройках хостинга.")

async def main():
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

# Исправленная точка входа (с двойными подчеркиваниями)
if name == "__main__":
    asyncio.run(main())
