from typing import Any

from fastapi import UploadFile
from sqlalchemy import text, select

from app.schemas.db_schemas import User as UserTable, SubscriptionPlan
from app.status_messages import StatusMessage
from draft import asession_maker


async def email_exists(email: str) -> bool:
    async with asession_maker() as session:
        result = await \
            session.execute(
                text(
                    f"select exists (select email from {UserTable.__tablename__} where email = '{email}') as has_data"))
        return result.one()[0]


async def add_user(user_to_db: UserTable):
    async with asession_maker() as session:
        session.add(user_to_db)
        await session.commit()


async def get_subscription_plan(subscription_plan_id: int) -> SubscriptionPlan:
    async with asession_maker() as session:
        stmt = select(SubscriptionPlan).where(SubscriptionPlan.id == subscription_plan_id)
        result = await session.execute(stmt)
        return result.one()[0]


async def check_credentials(email: str, hashed_password: str) -> StatusMessage:
    async with asession_maker() as session:
        stmt = select(UserTable.email, UserTable.password).where(UserTable.email == email)
        res = await session.execute(stmt)
        res = res.first()
        if res is None:
            return StatusMessage.no_such_email.value
        else:
            if res.password == hashed_password:
                return StatusMessage.ok.value
            return StatusMessage.wrong_password.value


if __name__ == '__main__':
    pass
    # import asyncio
    # from draft_but_mine import get_sessionmaker
    #
    # asm = get_sessionmaker()
    # asyncio.run(check_credentials(asm, 'hacker1@sobaka', '2'))
