from app.jwt_manager import JWTManager
import time
import asyncio


async def proof():
    token = await JWTManager.create_access_token(username="kirill_is_wrong")
    print(token)
    await JWTManager.decode_access(token)
    time.sleep(70)
    await JWTManager.decode_access(token)

if __name__ == '__main__':
    asyncio.run(proof())