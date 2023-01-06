import logging
from typing import Optional

from database.filtering import FILTER_MAP
from database.repositories import OrmRepository
from domain.artist.data import ArtistData, ArtistFiltersData
from domain.artist.models import Artist

logger = logging.getLogger("ArtistRepository")


class ArtistRepository(OrmRepository):
    """Repository to manage Artist objects."""

    def create_multiple_artists(self, artists: list) -> Optional[list[ArtistData]]:
        """Creates multiple artists registers.

        Args:
            artists: List of ArtistData objects.

        Returns:
            List of ArtistData objects.
        """
        try:
            new_artists = [Artist(name=artist.name, url_name=artist.url_name) for artist in artists]

            self.session.add_all(new_artists)
            self.session.commit()

            return [ArtistData.from_dict(artist.__dict__) for artist in artists]

        except Exception:
            logging.exception("Something happened while creating multiple artists.")
            return None

    def get_artists(self) -> Optional[list[ArtistData]]:
        """Retrieves all artists.

        Returns:
            List of ArtistData objects.
        """
        try:
            artists = self.session.query(Artist).all()

            return [ArtistData.from_dict(artist.__dict__) for artist in artists]

        except Exception:
            logging.exception("Something happened while retrieving artists.")
            return []

    def get_artist_by_id(self, artist_id: int) -> Optional[ArtistData]:
        """Retrieves an artist by its id.

        Args:
            artist_id: artist's unique identifier.

        Returns:
            ArtistData object.
        """
        try:
            artist = self.session.query(Artist).filter_by(id=artist_id).first()

            if not artist:
                return artist

            return ArtistData.from_dict(artist.__dict__)

        except Exception:
            logging.exception(f"Something happened while retrieving artist by id: {artist_id}.")
            return None

    def get_artists_filtered(self, filters: ArtistFiltersData) -> [list[ArtistData], int]:
        """Retrieves artists filtered by params.

        Args:
            filters: ArtistFilters object.

        Returns:
            artists: List of ArtistData objects
            count: total number of registers.
        """
        try:
            query = self.session.query(Artist)

            if filters.field:
                operator = FILTER_MAP.get(filters.operator)
                field = getattr(Artist, filters.field)

                query = operator(query=query, field=field, value=filters.value)

            artists = query.offset(filters.offset).limit(filters.limit).all()

            artist_count = query.count()

            artists = [ArtistData.from_dict(artist.__dict__) for artist in artists]

            return artists, artist_count

        except Exception:
            logging.exception("Something happened while retrieving artists filtered.")
            return []
