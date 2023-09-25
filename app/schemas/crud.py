from typing import Any, Dict

from sqlalchemy import text, select, update

from app.models.subscription_plan import SubscriptionPlanInfo
from app.models.context import ContextInfo, UserContextsInfo
from app.models.chat import AllUserChats, ChatInfo, ChatPdfInfo, ChatInfoIdName
from app.models.user import AuthorisedUserInfo
from app.schemas.db_schemas import User as UserTable, SubscriptionPlan as SubscriptionTable, Context, Chat
from app.status_messages import StatusMessage
from draft import asession_maker
from app.llm.apgvector import AsyncPgVector
import os


apgvector_instance = AsyncPgVector(
        user = os.environ.get('POSTGRES_USER'),
        password = os.environ.get('POSTGRES_PASSWORD'),
        host = os.environ.get('POSTGRES_HOST'),
        port = os.environ.get('POSTGRES_PORT'),
        database = os.environ.get('POSTGRES_DBNAME')
)

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


async def update_user(user_email: str, new_values: Dict[str, Any]):
    async with asession_maker() as session:
        stmt = update(UserTable).where(UserTable.email == user_email).values(new_values)
        await session.execute(stmt)
        await session.commit()


async def check_credentials(email: str, hashed_password: str) -> StatusMessage:
    async with asession_maker() as session:
        stmt = select(UserTable.email, UserTable.hashed_password).where(UserTable.email == email)
        res = await session.execute(stmt)
        res = res.first()
        if res is None:
            return StatusMessage.no_such_email.value
        else:
            if res.hashed_password == hashed_password:
                return StatusMessage.ok.value
            return StatusMessage.wrong_password.value


async def get_user_info(email: str) -> AuthorisedUserInfo:
    async with asession_maker() as session:
        stmt = select(UserTable).where(UserTable.email == email)
        res = await session.execute(stmt)
        res = res.first()[0]
        return AuthorisedUserInfo(id=res.id,
                                  email=res.email,
                                  name=res.name,
                                  surname=res.surname,
                                  # hashed_password=res.hashed_password,
                                  # confirmed_registration=res.confirmed_registration,
                                  num_of_requests_used=res.num_of_requests_used,
                                  num_of_contexts=res.num_of_contexts,
                                  subscription_plan_id=res.subscription_plan_id)


async def get_subscription_plan_info(subscription_plan: int) -> SubscriptionPlanInfo:
    async with asession_maker() as session:
        stmt = select(SubscriptionTable).where(SubscriptionTable.id == subscription_plan)
        res = await session.execute(stmt)
        res = res.first()[0]
        return SubscriptionPlanInfo(id=res.id,
                                    price=res.price,
                                    max_context_amount=res.max_context_amount,
                                    name=res.name,
                                    max_context_size=res.max_context_size,
                                    max_question_length=res.max_question_length
                                    )


async def add_context(context: Context) -> Context:
    async with asession_maker() as session:
        session.add(context)
        await session.commit()
        await session.refresh(context)
        return context


async def add_chat(chat: Chat):
    async with asession_maker() as session:
        session.add(chat)
        await session.commit()
        return chat


async def update_chat(chat_id: int, new_values: Dict[str, Any]):
    async with asession_maker() as session:
        stmt = update(Chat).where(Chat.id == chat_id).values(new_values)
        await session.execute(stmt)
        await session.commit()


async def get_chat_message_history_by_chat_id(chat_id: int):
    async with asession_maker() as session:
        stmt = select(Chat.message_history).where(Chat.id == chat_id)
        res = await session.execute(stmt)
        res = res.first()[0]
        return res


async def get_user_contexts_from_db(user_id: int):
    async with asession_maker() as session:
        stmt = select(Context).where(Context.user_id == user_id)
        res = await session.execute(stmt)
        res = res.fetchall()
        return UserContextsInfo(
            contexts=[
                ContextInfo(
                    id=el[0].id,
                    name=el[0].name,
                    user_id=el[0].user_id,
                    type=el[0].type,
                    size=el[0].size,
                    path=el[0].path
                ) for el in res
            ]
        )


async def get_chat_context_name_by_chat_id(chat_id: int):
    async with asession_maker() as session:
        stmt_context_id = select(Chat.context_id).where(Chat.id == chat_id)
        res_context_id = await session.execute(stmt_context_id)
        res_context_id = res_context_id.first()[0]

        stmt = select(Context.name).where(Context.id == res_context_id)
        res = await session.scalar(stmt)
        return res



async def get_chatinfo_by_chat_id(chat_id: int):
    async with asession_maker() as session:
        stmt = select(Chat).where(Chat.id == chat_id)
        res = await session.execute(stmt)
        res = res.first()[0]
        cntx_id, msg_history = res.context_id, res.message_history

        stmt = select(Context.name).where(Context.id == cntx_id)
        cntx_name = await session.scalar(stmt)

        return ChatPdfInfo(
            message_history=msg_history,
            pdf_url='http://viewer.lovelogo.ru/' + cntx_name
        )


async def get_user_chats_from_db(user_id: int):
    async with asession_maker() as session:
        stmt = select(Chat).where(Chat.user_id == user_id)
        res = await session.execute(stmt)
        res = res.fetchall()
        return AllUserChats(
            chats=[
                ChatInfoIdName(
                    id=el[0].id,
                    name=el[0].name,
                ) for el in res
            ]
        )


if __name__ == '__main__':
    # pass
    import asyncio
    import json
    from draft_but_mine import get_sessionmaker

    asm = get_sessionmaker()
    # asyncio.run(update_chat(1, {'message_history': json.dumps(["system", "You are a helpful AI bot."])}))
    qwer = json.loads(asyncio.run(get_chat_message_history_by_chat_id(5)))

    print(qwer)
