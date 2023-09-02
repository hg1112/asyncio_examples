import asyncio
from platform import version
import asyncpg
from asyncpg.pool import connection

async def main():
    connection = await asyncpg.connect( host='127.0.0.1', user='postgres', database='postgres', password='opensource')
    version = connection.get_server_version()
    print(f'Connected! Postgres version is {version}')
    await connection.close()
asyncio.run(main())
