from hashlib import sha256


async def password_encoder(password: str) -> str:
    return str(sha256(password.encode('utf-8')).hexdigest())
