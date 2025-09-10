from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import Config

import boto3


config = Config.load()
engine = create_async_engine("postgresql+asyncpg://postgres:0000@127.0.0.1:5432/pastebin", echo=True)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass