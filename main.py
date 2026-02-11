import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Загружаем ключи
TOKEN = os.getenv("BOT_TOKEN")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Настройка модели (упрощенный вариант без лишних путей)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Бот запущен! Напиши мне что-нибудь.")

@dp.message()
async def chat(message: types.Message):
    if not message.text:
        return
    try:
        # Прямое обращение к модели
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        print(f"Ошибка Gemini: {e}")
        await message.answer("Произошла ошибка при генерации ответа.")

async def main():
    # Перед запуском удаляем вебхуки, чтобы убрать ошибку Conflict
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
