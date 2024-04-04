import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from middlewares.db import CounterMiddleware
from handlers.user_private import user_private_router


TOKEN = "6521597625:AAGnXGtc4s7UHnjheO3PpjAeD2CjQTgDCJ0"
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

dp = Dispatcher()

user_private_router.message.middleware(CounterMiddleware())

dp.include_router(user_private_router)


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
