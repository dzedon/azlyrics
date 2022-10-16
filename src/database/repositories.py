"""Provide base clases for database-based repositories."""
from abc import ABC

from sqlalchemy.orm import Session


class OrmRepository(ABC):
    """Provides a base class tu use repositories with database session."""

    def __init__(self, *, session: Session):
        """Initialize the repository with a session."""
        super().__init__()

        self.session: Session = session
