import asyncio
from typing import final
import asyncpg
from asyncpg.pool import logging

# Example : successful transaction
# async def main():
#     connection = await asyncpg.connect(
#             host='127.0.0.1',
#             port = 5432,
#             database='products',
#             user='postgres',
#             password='opensource'
#             )

#     async with connection.transaction():
#         await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_1')")
#         await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_2')")

#     query = """
#     SELECT brand_name FROM brand
#     WHERE brand_name LIKE 'brand%'
#     """

#     brands = await connection.fetch(query)
#     print(brands)

#     await connection.close()

# asyncio.run(main())


# Example : successful transaction with exception handling
# async def main():
#     connection = await asyncpg.connect(
#             host='127.0.0.1',
#             port = 5432,
#             database='products',
#             user='postgres',
#             password='opensource'
#             )

#     try:
#         async with connection.transaction():
#             await connection.execute("INSERT INTO brand VALUES(9999, 'brand_3')")
#             await connection.execute("INSERT INTO brand VALUES(9999, 'brand_3')")
#     except Exception as e:
#         logging.exception("Error with running transaction ", e)
#     finally:
#         query = """
#         SELECT brand_name FROM brand
#         WHERE brand_name LIKE 'brand%'
#         """
#         brands = await connection.fetch(query)
#         print(brands)
#         await connection.close()

# asyncio.run(main())

# Example 3 : successful nested transaction with exception handling
async def main():
    connection = await asyncpg.connect(
            host='127.0.0.1',
            port = 5432,
            database='products',
            user='postgres',
            password='opensource'
            )

    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'new_brand')")
        try:
            async with connection.transaction():
                await connection.execute("INSERT INTO brand VALUES(1, 'already exists')")
        except Exception as e:
            logging.exception("Error with running transaction ", e)
    query = """
    SELECT brand_name FROM brand
    WHERE brand_name LIKE '%brand%'
    """
    brands = await connection.fetch(query)
    print(brands)
    await connection.close()

asyncio.run(main())
