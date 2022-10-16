import logging
from typing import Optional

from database.filtering import FILTER_MAP
from database.repositories import OrmRepository
from domain.album.data import AlbumData, AlbumFiltersData
from domain.album.models import Album
from domain.album.schemas import AlbumSchema

logger = logging.getLogger("AZ_LYRICS")


class AlbumRepository(OrmRepository):
    """Album Repository."""

    def create_multiple_albums(self, albums: list, artist_id: int) -> Optional[list[AlbumData]]:
        """Creates multiple albums registers.

        Args:
            albums: List of AlbumSchema objects.
            artist_id: artist unique identifier.

        Returns:
            List of AlbumSchema objects.
        """
        try:
            new_albums = [Album(name=album, artist_id=artist_id) for album in albums]

            self.session.add_all(new_albums)
            self.session.commit()

            # return [AlbumData.from_dict(album.__dict__) for album in new_albums] # noqa: E501
            return new_albums

        except Exception:
            logging.exception("Something happened while creating multiple albums")
            return None

    def get_albums(self) -> Optional[list[AlbumSchema]]:
        """Retrieves all albums.

        Returns:
            List of AlbumData objects.
        """
        try:
            albums = self.session.query(Album).all()

            return [AlbumData.from_dict(album.__dict__) for album in albums]

        except Exception:
            logging.exception("Something happened while retrieving all albums")
            return None

    def get_album_by_id(self, album_id: int) -> Optional[AlbumData]:
        """Retrieves an album by its id.

        Args:
            album_id: album unique identifier.

        Returns:
            AlbumData object.
        """
        try:
            album = self.session.query(Album).filter(Album.id == album_id).first()

            if not album:
                return album

            return AlbumData.from_dict(album.__dict__)

        except Exception:
            logging.exception(f"Something happened while retrieving album with id: {album_id}")
            return None

    def get_albums_filtered(self, filters: list[AlbumFiltersData]):
        """Retrieves album filtered by params.

        Args:
            filters: AlbumFiltersData object.

        Returns:
            albums: List of AlbumData objects
            count: total number of registers.
        """
        try:
            query = self.session.query(Album)

            if filters.field:
                operator = FILTER_MAP.get(filters.operator)
                field = getattr(Album, filters.field)

                query = operator(query=query, field=field, value=filters.value)

            albums = query.offset(filters.offset).limit(filters.limit).all()

            album_count = query.count()

            songs = [AlbumData.from_dict(album.__dict__) for album in albums]

            return songs, album_count

        except Exception:
            logging.exception("Something happened while retrieving albums filtered.")
            return []
