from async_db.sql import PRODUCTS_QUERY
import asyncpg
import asyncio 
from util import async_timed, delay

# Example : async generators

# async def pos_async(until: int):
#     for i in range(1, until):
#         await delay(i)
#         yield i

# @async_timed()
# async def main():
#     ag = pos_async(3)
#     print(type(ag))
#     async for n in ag:
#         print(f'Generator {n}')

# asyncio.run(main())

# asynchronous generators utilizing postgres cursor

# async def main():
#     connection = await asyncpg.connect(
#             host='127.0.01',
#             port = 5432,
#             database='products',
#             user='postgres',
#             password='opensource'
#             )
#     async with connection.transaction():
#         async for product in connection.cursor(PRODUCTS_QUERY):
#             print(product)

# asyncio.run(main())

async def main():
    connection = await asyncpg.connect(
            host='127.0.01',
            port = 5432,
            database='products',
            user='postgres',
            password='opensource'
            )
    async with connection.transaction():
        cursor = await connection.cursor(PRODUCTS_QUERY)
        await cursor.forward(500)
        products = await cursor.fetch(100)
        for product in products:
            print(product)

    await connection.close()

asyncio.run(main())
