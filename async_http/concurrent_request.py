import asyncio
import aiohttp
from aiohttp import ClientSession
from util import delay, fetch_status, async_timed


# Example 1 : Gen coroutines and await them 
## gather returns iff all of coroutines (wrapped as tasks) finish
# @async_timed()
# async def main():
#     async with aiohttp.ClientSession() as session:
#         urls = ['http://www.example.com' for _ in range(1000)]
#         requests = [fetch_status(session , url) for url in urls]
#         statuses = await asyncio.gather(*requests)
#         print(statuses)

# asyncio.run(main())


# Example 2 : order of execution maintained 
# @async_timed()
# async def main():
#     two, one = await asyncio.gather(delay(2), delay(1))
#     print(one, two)

# asyncio.run(main())


# Example 3 : return exceptions (fail early)
# @async_timed()
# async def main():
#     urls = ['https://nouchurl.com', 'https://www.example.com']
#     async with aiohttp.ClientSession() as session:
#         requests = [fetch_status(session, url) for url in urls]
#         result = await asyncio.gather(*requests)
#         print(result)

# asyncio.run(main())

# Example 4 : return exceptions (fail but graceful collection of errors)
@async_timed()
async def main():
    urls = ['https://nouchurl.com', 'https://www.example.com']
    async with aiohttp.ClientSession() as session:
        requests = [fetch_status(session, url) for url in urls]
        error, valid = await asyncio.gather(*requests, return_exceptions=True)
        print(valid)
        print(error)

asyncio.run(main())
