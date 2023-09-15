import asyncio
import time

def long():
    for _ in range(100_000_000):
        pass
    return 'lol('


async def call_pgvector():
    a = await asyncio.to_thread(long)
    return a


async def main():
    tasks = [call_pgvector(), call_pgvector()]
    await asyncio.gather(*tasks)
    return 'fuk'

if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(f'{time.time() - start} seconds')
