"""Defines fastapi dependencies to interact with database."""
from typing import TypeVar


from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from .repositories import OrmRepository
from .session import session

# Any children of OrmRepository
_T = TypeVar("_T", bound=OrmRepository)


def get_connection_status(session: Session = session) -> str:
    """Return the database connection status."""
    from settings import settings

    db_status: str = "unable to connect"

    try:
        result = session.execute(select(1)).fetchone()

        if result:
            db_status = "connected"
    except OperationalError as e:
        print(e)

        if settings.debug:
            # SQLA Operational errors wraps DB-API exceptions from the driver
            db_status = e.args
    except Exception as e:
        print(e)

    return db_status
