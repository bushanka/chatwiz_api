from fastapi import UploadFile
from sqlalchemy import text, select
from .db_schemas import User as UserTable, SubscriptionPlan


async def email_exists(ses_maker, email: str) -> bool:
    async with ses_maker() as session:
        result = await \
            session.execute(
                text(
                    f"select exists (select email from {UserTable.__tablename__} where email = '{email}') as has_data"))
        return result.one()[0]


async def add_user(ses_maker, user_to_db: UserTable):
    async with ses_maker() as session:
        session.add(user_to_db)
        await session.commit()


async def get_subscription_plan(ses_maker, subscription_plan_id: int) -> SubscriptionPlan:
    async with ses_maker() as session:
        stmt = select(SubscriptionPlan).where(SubscriptionPlan.id == subscription_plan_id)
        result = await session.execute(stmt)
        return result.one()[0]