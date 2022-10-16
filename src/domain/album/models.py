from sqlalchemy import Column, ForeignKey, Integer

from database.mixins import Identified, Named, TimeStamped
from database.registries import default_registry


@default_registry.mapped
class Album(Identified, Named, TimeStamped):
    """Album model."""

    __tablename__ = "album"

    artist_id = Column(Integer, ForeignKey("artist.id"), nullable=False)
