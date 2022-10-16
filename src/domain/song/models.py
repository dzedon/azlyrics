from sqlalchemy import Column, ForeignKey, Integer

from database.mixins import Identified, Named, TimeStamped
from database.registries import default_registry


@default_registry.mapped
class Song(Identified, Named, TimeStamped):
    """Song model."""

    __tablename__ = "song"

    album_id = Column(Integer, ForeignKey("album.id"), nullable=False)
