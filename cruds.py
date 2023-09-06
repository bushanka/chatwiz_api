"""
Тут прописываем операции по взаимодействию с БД
"""
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from db_models.users import User
from pydantic_models.user_models import SignUpUser

from hashlib import sha256

os.environ['db_user'] = 'some_user'
os.environ['db_password'] = '111'
os.environ['db_host'] = '127.0.0.1'
os.environ['db_name'] = 'linkup'

session_maker = sessionmaker(create_engine(
    f'postgresql+psycopg2://{os.environ["db_user"]}:{os.environ["db_password"]}@'
    f'{os.environ["db_host"]}/{os.environ["db_name"]}'
))


def password_encoder(password: str) -> str:
    return str(sha256(password.encode('utf-8')).hexdigest())


def get_emails():  # not sure if it's the best way
    with session_maker() as session:
        stmt = select(User.email)
        return set(session.execute(stmt).fetchall())


def create_sign_up_user(su_user: SignUpUser):  # todo разобраться какие ошибки тут могут возвращаться
    with session_maker() as session:
        if (su_user.email.ascii_email,) in get_emails():
            return 'NO no no'
        if su_user.has_good_password():
            user_to_db = User(email=su_user.email.ascii_email,
                              password=password_encoder(su_user.password))
            session.add(user_to_db)
            session.commit()
            return 'Super cool'
