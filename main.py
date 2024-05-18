import logging
import asyncio
from bot import dp
from bot import bot

async def main():
    await dp.start_polling(bot)


if __name__ =="__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())