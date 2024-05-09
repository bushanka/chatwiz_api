from hashlib import sha256


async def password_encoder(password: str) -> str:
    """
    Хэширование пароля.
    :param password: пароль юзера
    :return: захэшированный пароль юзера
    """
    return str(sha256(password.encode('utf-8')).hexdigest())
