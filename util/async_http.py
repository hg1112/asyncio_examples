from aiohttp import ClientSession
from util import delay

async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status

async def fetch_status_delayed(session: ClientSession, url: str, delay_seconds: int) -> int:
    await delay(delay_seconds)
    async with session.get(url) as result:
        return result.status
