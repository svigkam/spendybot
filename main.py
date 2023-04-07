from aiogram import Bot, Dispatcher, executor
from utils.config import API_TOKEN, logging_config
from repositories import db_repo as db
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    await db.init()
    logging_config()


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
