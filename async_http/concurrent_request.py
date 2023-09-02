import asyncio
import logging
from concurrent.futures import FIRST_COMPLETED, FIRST_EXCEPTION, as_completed
import aiohttp
from aiohttp import ClientSession
from util import delay, fetch_status, async_timed
from util.async_http import fetch_status_delayed

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
# @async_timed()
# async def main():
#     urls = ['https://nouchurl.com', 'https://www.example.com']
#     async with aiohttp.ClientSession() as session:
#         requests = [fetch_status(session, url) for url in urls]
#         error, valid = await asyncio.gather(*requests, return_exceptions=True)
#         print(valid)
#         print(error)

# asyncio.run(main())

# Example 5: Uneven distributed response times
# @async_timed()
# async def main():
#     async with aiohttp.ClientSession() as session:
#         fetches = [
#                 fetch_status(session, 'http://www.example.com'),
#                 fetch_status_delayed(session, 'http://www.example.com', 10),
#                 fetch_status_delayed(session, 'http://www.example.com', 5)
#                 ]
#         for finished in asyncio.as_completed(fetches):
#             print(await finished)
#     
# asyncio.run(main())

# Example 5: Uneven distributed response times with timeout
# @async_timed()
# async def main():
#     async with aiohttp.ClientSession() as session:
#         fetches = [
#                 fetch_status(session, 'http://www.example.com'),
#                 fetch_status_delayed(session, 'http://www.example.com', 10),
#                 fetch_status_delayed(session, 'http://www.example.com', 5)
#                 ]
#         for finished in asyncio.as_completed(fetches, timeout=6):
#             try:
#                 result = await finished
#                 print(result)
#             except asyncio.TimeoutError:
#                 print('Timeout error')
#         for task in asyncio.all_tasks():
#             print(task)

#     
#     
# asyncio.run(main())


# Example 6: wait - default 

# @async_timed()
# async def main():
#     async with ClientSession() as session:
#         fetches = [
#                 asyncio.create_task(fetch_status(session, 'https://www.example.com')),
#                 asyncio.create_task(fetch_status(session, 'https://www.example.com'))
#                 ]
#         done, pending = await asyncio.wait(fetches)
#         print(f'Completed {len(done)} tasks')
#         print(f'Pending {len(pending)} tasks')

## done_task is guaranteed a completed future (success/failure)
#         for done_task in done:
#             result = await done_task
#             print(result)

# asyncio.run(main())


# Example 7: wait - ALL_COMPLETED
# @async_timed()
# async def main():
#     async with ClientSession() as session:
#         good = fetch_status(session, 'https://www.example.com')
#         bad = fetch_status(session, 'http://nosuchurl')
#         fetches = [
#                 asyncio.create_task(good),
#                 asyncio.create_task(bad)
#                 ]
#         done, pending = await asyncio.wait(fetches)
#         print(f'Completed {len(done)} tasks')
#         print(f'Pending {len(pending)} tasks')
#         for done_task in done:

#             if done_task.exception():
#                 logging.error("Request faild with exception ", exc_info=done_task.exception())
#             else:
#                 print(f"Success : {done_task.result()}")

# asyncio.run(main())

# Example 8 : wait - FIRST_EXCEPTION
# @async_timed()
# async def main():
#     async with ClientSession() as session:
#         
#         fetches = [
#                 asyncio.create_task(fetch_status(session,'pytohn://bad.com')),
#                 asyncio.create_task(fetch_status_delayed(session, 'https://www.example.com', 3)),
#                 asyncio.create_task(fetch_status_delayed(session, 'https://www.example.com', 3))
#                 ]
#         done, pending = await asyncio.wait(fetches, return_when=FIRST_EXCEPTION)
#         print(f'Completed {len(done)} tasks')
#         print(f'Pending {len(pending)} tasks')
#         for done_task in done:
#             if done_task.exception():
#                 logging.error("Request faild with exception ", exc_info=done_task.exception())
#             else:
#                 print(f"Success : {done_task.result()}")
#         for task in pending:
#             task.cancel()
# asyncio.run(main())

# Example 8 : wait - FIRST_COMPLETED , but process others as they complete similar to as_completed
# @async_timed()
# async def main():
#     async with ClientSession() as session:
#         
#         pending = [
#                 asyncio.create_task(fetch_status(session, 'https://www.example.com')),
#                 asyncio.create_task(fetch_status(session, 'https://www.example.com')),
#                 asyncio.create_task(fetch_status(session, 'https://www.example.com'))
#                 ]
#         while pending:
#             done, pending = await asyncio.wait(pending, return_when=FIRST_COMPLETED)
#             print(f'Completed {len(done)} tasks')
#             print(f'Pending {len(pending)} tasks')
#             for done_task in done:
#                 print(await done_task)
# asyncio.run(main())

# Example 9 : wait - exception handling

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://exmaple.com'
        fetchers = [
                asyncio.create_task(fetch_status(session, url)),
                asyncio.create_task(fetch_status(session, url)),
                asyncio.create_task(fetch_status_delayed(session, url, 3)),
                ]
        done, pending = await asyncio.wait(fetchers, timeout=1)
        print(f'Completed {len(done)} tasks')
        print(f'Pending {len(pending)} tasks')
        for done_task in done:
            print(await done_task)

asyncio.run(main())

