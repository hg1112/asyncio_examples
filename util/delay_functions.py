import asyncio


async def delay(n: int) -> int:
    print(f"start sleeping ...")
    await asyncio.sleep(n)
    print(f"finished sleeping {n} seconds.")
    return n
