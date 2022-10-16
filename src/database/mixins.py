from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql.functions import now as sql_now


class Identified:
    """Provides an integer primary key to uniquely identify the model."""

    id = Column(Integer, primary_key=True)


class Named:
    """Provides a string name to identify the model."""

    name = Column(String(50), nullable=False)


class TimeStamped:
    """Provides created_at and updated_at columns to track the model's creation and update."""

    created_at = Column(DateTime, nullable=False, server_default=sql_now())
    updated_at = Column(DateTime, nullable=False, server_default=sql_now())
