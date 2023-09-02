import asyncio
import asyncpg
from asyncpg import Record, connect, connection
from sql import *
from random import sample, randint
from typing import List, Tuple, Union
from util import async_timed

# Create tables
# async def main():
#     connection = await asyncpg.connect(
#             host='127.0.0.1',
#             port=5432,
#             user='postgres',
#             database='products',
#             password='opensource'
#             )
#     statements = [
#             CREATE_BRAND_TABLE,
#             CREATE_PRODUCT_TABLE,
#             CREATE_PRODUCT_SIZE_TABLE,
#             CREATE_PRODUCT_COLOR_TABLE,
#             CREATE_SKU_TABLE,
#             SIZE_INSERT,
#             COLOR_INSERT
#             ]

#     print('Creating products database')
#     for statement in statements:
#         status = await connection.execute(statement)
#         print('SQL : ', statement)
#         print(status)

#     print('Finished creating products database')
#     await connection.close()

# asyncio.run(main())


# select all brands 
# async def main():
#     connection = await asyncpg.connect(
#             host='127.0.0.1',
#             port=5432,
#             database='products',
#             user='postgres',
#             password='opensource'
#             )

#     await connection.execute("INSERT INTO brand VALUEs (DEFAULT, 'Levis')")
#     await connection.execute("INSERT INTO brand VALUEs (DEFAULT, 'Seven')")

#     brands_query = 'SELECT brand_id, brand_name FROM brand'

#     results: list[Record] = await connection.fetch(brands_query)
#     for brand in results:
#         print(f'id : {brand["brand_id"]}, name: {brand["brand_name"]}')

#     await connection.close()

# asyncio.run(main())


# concurrent queries in asyncio event loop
# def load_common_words() -> List[str]:
#     with open('async_db/common_words.txt') as common_words:
#         return common_words.readlines()

# def generate_brand_names(words: List[str]) -> List[Tuple[Union[str, ]]]:
#     return [(words[index], ) for index in sample(range(100), 100)]


# async def insert_brands(common_words, connection) -> int:
#     brands = generate_brand_names(common_words)
#     insert_brands = "INSERT INTO brand VALUES (DEFAULT, $1)"
#     return await connection.executemany(insert_brands, brands)

# async def main():
#     connection = await asyncpg.connect(
#             host='127.0.0.1',
#             port=5432,
#             database='products',
#             user='postgres',
#             password = 'opensource'
#             )
#     common_words = load_common_words()
#     await insert_brands(common_words, connection)

# asyncio.run(main())

# def gen_products(common_words: List[str], brand_id_start: int, brand_id_end: int, products_to_create: int) -> List[Tuple[str, int]]:
#     products = []
#     for _ in range(products_to_create):
#         description = [common_words[index] for index in sample(range(100), 100)]
#         brand_id = randint(brand_id_start, brand_id_end)
#         products.append(("".join(description), brand_id))
#     return products

# def gen_skus(product_id_start: int, product_id_end: int, skus_to_create:int) -> List[Tuple[int, int, int]]:
#     skus = []
#     for _ in range(skus_to_create):
#         product_id = randint(product_id_start, product_id_end)
#         size_id = randint(1, 3)
#         color_id = randint(1, 2)
#         skus.append((product_id, size_id, color_id))
#     return skus

# async def main():
#     connection = await asyncpg.connect(
#             host='127.0.0.1',
#             port=5432,
#             database='products',
#             user='postgres',
#             password = 'opensource'
#             )
#     common_words = load_common_words()
#     await insert_brands(common_words, connection)
#     products = gen_products(common_words, 1, 100, 1000)
#     await connection.executemany( 
#             "INSERT INTO product VALUES(DEFAULT, $1 , $2)", products)
#     skus = gen_skus(1, 1000, 100000)
#     await connection.executemany(
#             "INSERT INTO sku VALUES (DEFAULT, $1, $2, $3)", skus
#             )

#     await connection.close()

# asyncio.run(main())


# Example showing limitations of single connection to db
# async def main():
#     connection = await asyncpg.connect(
#             host = '127.0.0.1',
#             port = 5432,
#             database='products',
#             user='postgres',
#             password = 'opensource'
#             )

#     fetches =[connection.execute(PRODUCT_QUERY), connection.execute(PRODUCT_QUERY)]
#     results = await asyncio.gather(*fetches)

# asyncio.run(main())

# Example : async connection pools 

# async def product_query(pool):
#     async with pool.acquire() as connection:
#         await connection.fetchrow(PRODUCT_QUERY)

# async def main():
#     async with asyncpg.create_pool(
#             host='127.0.0.1', 
#             port = 5432, 
#             database='products', 
#             user='postgres', 
#             password = 'opensource', 
#             min_size = 6,
#             max_size = 6) as pool:
#         await asyncio.gather(product_query(pool), product_query(pool))

# asyncio.run(main())


# Example : sync vs async

async def product_query(pool):
    async with pool.acquire() as connection:
        await connection.fetch(PRODUCT_QUERY)

@async_timed()
async def query_sync(pool, queries):
    return [await product_query(pool) for _ in range(queries)]

@async_timed()
async def query_async(pool, queries):
    queries = [product_query(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)

async def main():
    async with asyncpg.create_pool(
            host='127.0.0.1', 
            port = 5432, 
            database='products', 
            user='postgres', 
            password = 'opensource', 
            min_size = 6,
            max_size = 6) as pool:
        await query_sync(pool, 10000)
        await query_async(pool, 10000)

asyncio.run(main())
