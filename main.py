import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# Загружаем ключи
TOKEN = os.getenv("BOT_TOKEN")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Настройка модели
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Бот запущен! Я готов к общению.")

@dp.message()
async def chat(message: types.Message):
    if not message.text:
        return

    text = message.text.lower()

    # Специфический ответ про создателя
    if "создатель" in text or "кто тебя создал" in text or "кто твой создатель" in text:
        await message.answer("Моим создателем является корпорация Geshan Co.")
        return

    try:
        # Обращение к Gemini
        response = model.generate_content(message.text)
        await message.answer(response.text)
    
    except Exception as e:
        # Предохранитель для ошибки 429 (лимиты)
        if "429" in str(e):
            await message.answer("Ой! Я получил слишком много вопросов и мне нужно немного отдохнуть (лимит запросов). Попробуй написать мне через минуту! ☕")
        else:
            print(f"Ошибка Gemini: {e}")
            await message.answer("Произошла ошибка при генерации ответа. Попробуй позже.")

async def main():
    # Очистка очереди (убирает Conflict)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
