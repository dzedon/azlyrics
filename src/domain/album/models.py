from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint

from database.mixins import Identified, Named, TimeStamped
from database.registries import default_registry


@default_registry.mapped
class Album(Identified, Named, TimeStamped):

    __tablename__ = "album"

    artist_id = Column(Integer, ForeignKey("artist.id"), nullable=False)