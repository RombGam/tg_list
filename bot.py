import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import pytz
import os
from datetime import datetime, time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def send_morning_poll():
    question = "Сегодня"
    options = ["я есть", "нет по уважу", "нет по неуважу", "опаздываю"]
    
    try:
        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            is_anonymous=False,
            allows_multiple_answers=False
        )
        logger.info("Опрос отправлен успешно!")
    except Exception as e:
        logger.error(f"Ошибка: {e}")

@dp.message(Command("getid"))
async def get_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"Chat ID: {chat_id}")

async def poll_scheduler():
    """Простой планировщик на asyncio"""
    while True:
        now = datetime.now().time()
        target_time = time(0, 46)  # 00:46
        
        if now.hour == target_time.hour and now.minute == target_time.minute:
            await send_morning_poll()
            # Ждем 61 секунду чтобы не отправить дважды
            await asyncio.sleep(61)
        else:
            # Проверяем каждую минуту
            await asyncio.sleep(60)

async def main():
    # Запускаем планировщик в фоне
    asyncio.create_task(poll_scheduler())
    
    logger.info("Бот запущен с простым планировщиком")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
