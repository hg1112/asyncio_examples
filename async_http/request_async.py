import asyncio
import aiohttp

from aiohttp import ClientSession
from util import async_timed

@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    ten_milli = aiohttp.ClientTimeout(total=0.01)
    async with session.get(url, timeout=ten_milli) as result:
        return result.status


@async_timed()
async def main():
    session_timeout = aiohttp.ClientTimeout(total=1, connect=0.1)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        url = 'https://www.example.com'
        status = await fetch_status(session, url)
        print(f'Status for {url} was {status}')


asyncio.run(main())
