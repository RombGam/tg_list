import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import PollOption
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

# Добавьте в начало файла
import logging
logging.basicConfig(level=logging.INFO)

# В функции main добавьте:
async def main():
    logging.info("Запуск бота...")
    # остальной код...

# Замените на ваш токен бота
BOT_TOKEN = "8345910104:AAH5y2PSsom_SWSIjEFHgP71jo3ALIapXEA"
# Замените на ID вашей группы (например: -1001234567890)
CHAT_ID = "-1002941578906"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  # Создаем Dispatcher без аргументов

# Функция для отправки опроса
async def send_morning_poll():
    question = "Сегодня"
    options = [
        "я  есть",
        "нет по уважу",
        "нет по неуважу",
        "опаздываю"
    ]
    
    try:
        await bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            is_anonymous=False,
            allows_multiple_answers=False
        )
        print("Опрос отправлен успешно!")
    except Exception as e:
        print(f"Ошибка отправки опроса: {e}")

# Функция для получения ID чата (новый синтаксис aiogram 3.x)
@dp.message(Command("getid"))
async def get_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"Chat ID этой группы: {chat_id}")

# Настройка планировщика
async def scheduler():
    timezone = pytz.timezone("Europe/Moscow")  # Укажите вашу временную зону
    scheduler = AsyncIOScheduler(timezone=timezone)
    
    # Отправлять каждый день в 9:00 утра
    scheduler.add_job(
        send_morning_poll,
        trigger=CronTrigger(hour=1, minute=34 ),
        misfire_grace_time=60
    )
    
    scheduler.start()

# Запуск бота
async def main():
    await scheduler()
    # Убедитесь, что бот инициализирован в диспетчере
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
