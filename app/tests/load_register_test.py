import asyncio
import aiohttp
import time

async def send_request(session, email):
    url = f'http://127.0.0.1:8000/users/register?email={email}&password=123&name=baby&surname=tape'
    async with session.post(url, headers={"accept": "application/json"}) as response:
        response_text = await response.text()
        print(response_text)
    print(f"Email: {email} registered")

async def main():
    emails = [f"hacker{i}@sobaka" for i in range(1, 3)]
    async with aiohttp.ClientSession() as session:
        tasks = []
        for email in emails:
            task = asyncio.create_task(send_request(session, email))
            tasks.append(task)

        start_time = time.time()
        await asyncio.gather(*tasks)
        end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())