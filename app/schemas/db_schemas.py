#  Модули, определяющие модели данных для вашей базы данных. 
# Тут описываем наш ORM, такой как SQLAlchemy, для определения моделей данных.
import datetime
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    ...


class User(Base):
    """
    Table for storing users.
    """
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    subscription_plan_id = Column(Integer, nullable=False, default=1)
    action_points_used = Column(Integer, nullable=False, default=0)


class SubscriptionPlan(Base):
    """
    Table for storing subscription plans.
    """
    __tablename__ = "subscription_plan"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    name = Column(String(255))
    price = Column(Float, nullable=False)
    max_context_amount = Column(Integer, nullable=False)
    max_context_size = Column(Integer, nullable=False)
    max_question_length = Column(Integer, nullable=False)
    max_action_points = Column(Integer, nullable=False)


class Context(Base):
    """
    Table for storing contexts.
    """
    __tablename__ = "contexts"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, )
    user_id = Column(Integer, nullable=False, )
    type = Column(String(255), nullable=False, )
    size = Column(Float, nullable=False, )
    path = Column(String(255), nullable=False, )
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)


class Chat(Base):
    """
    Table for storing chats.
    """
    __tablename__ = "chats"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, nullable=False)
    context_id = Column(Integer, nullable=True)
    message_history = Column(JSON, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)


class Feedback(Base):
    """
    Table for storing feedbacks.
    """
    __tablename__ = "feedbacks"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    comment_text = Column(String(1000), nullable=False)



