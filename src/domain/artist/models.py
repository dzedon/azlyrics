from sqlalchemy import Column, String

from database.mixins import Identified, Named, TimeStamped
from database.registries import default_registry


@default_registry.mapped
class Artist(Identified, Named, TimeStamped):

    __tablename__ = "artist"

    url_name = Column(String(50), nullable=False)

