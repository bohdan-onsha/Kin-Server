import asyncio
import firebase_service

import sys

email, password = sys.argv[1:]


async def reg():
    try:
        await firebase_service.register(email, password, is_admin=True)
        print('Everything is ok')
    except:
        print('Something went wrong')


asyncio.run(reg())
