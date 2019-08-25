import asyncio
import firebase_service

import sys

email, password = sys.argv[1:]


async def reg():
    try:
        await firebase_service.register(email, password, is_admin=True)
        print('Created admin user.')
    except:
        print('Something went wrong, check firebase confing and try again.')


asyncio.run(reg())
