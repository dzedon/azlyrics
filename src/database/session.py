from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings


def get_engine(settings):
    return create_engine(
        settings.database_uri,
        pool_pre_ping=True,
    )


def get_session_maker(engine):
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )


def session() -> Generator:
    """
    Return a database session.

    This function is intended to be used as a FastAPI dependency.
    """

    try:
        db = session_maker()

        yield db
    finally:
        db.close()


engine = get_engine(settings)

session_maker = get_session_maker(engine)



