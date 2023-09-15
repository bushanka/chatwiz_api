#  Модули, определяющие модели данных для вашей базы данных. 
# Тут описываем наш ORM, такой как SQLAlchemy, для определения моделей данных.
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    subscription_plan_id = Column(Integer, nullable=False)
    num_of_requests_used = Column(Integer, nullable=False)
    num_of_contents = Column(Integer, nullable=False)


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plan"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    name = Column(String(255))
    price = Column(Float, nullable=False)
    max_content_amount = Column(Integer, nullable=False)
    max_content_size = Column(Integer, nullable=False)
    max_question_length = Column(Integer, nullable=False)


class Context(Base):
    __tablename__ = "contents"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, )
    user_id = Column(Integer, nullable=False, )
    type = Column(String(255), nullable=False, )
    size = Column(Float, nullable=False, )
    path = Column(String(255), nullable=False, )
