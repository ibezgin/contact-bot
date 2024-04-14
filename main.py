import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import router



Token = ("Тут должен быть ваш токен")
bot = Bot(token=Token)
dp = Dispatcher()



async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")