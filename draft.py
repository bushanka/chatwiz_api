from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

import os

load_dotenv()
args = {
    "host": os.getenv("POSTGRES_HOST"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DBNAME"),
    "port": os.getenv("POSTGRES_PORT"),
}

engine = create_async_engine(
    f"postgresql+asyncpg://{args['user']}:{args['password']}@{args['host']}/{args['dbname']}",
    echo=True,
)

asession_maker = async_sessionmaker(engine, expire_on_commit=False)