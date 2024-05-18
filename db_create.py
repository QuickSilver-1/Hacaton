from asyncio import get_event_loop
from config import config_1
from database import db


async def db_create():
    await db.set_bind(config_1.POSTGRES_URL)
    await db.gino.drop_all()
    await db.gino.create_all()



async def db_test():
    await db_create()

loop = get_event_loop()
loop.run_until_complete(db_test())
