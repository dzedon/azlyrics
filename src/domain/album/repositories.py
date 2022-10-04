from typing import Optional
import logging

from database.repositories import OrmRepository
from domain.album.models import Album
from domain.album.schemas import AlbumSchema

logger = logging.getLogger("AZ_LYRICS")

class AlbumRepository(OrmRepository):

    def create_album(self, album: AlbumSchema) -> Optional[AlbumSchema]:
        """Creates a new album register.

        Args:
            album: AlbumSchema object.

        Returns:
            AlbumSchema object.
        """
        try:
            new_album = Album(
                name=album.name,
                artist_id=album.artist_id
            )

            self.session.add(new_album)
            self.session.commit()

            return AlbumSchema.dump(new_album)

        except Exception:
            logging.info("Something happened while creating a album {album.name}")
            return None

    def create_multiple_albums(self, albums: list) -> Optional[list[AlbumSchema]]:
        """Creates multiple albums registers.

        Args:
            albums: List of AlbumSchema objects.

        Returns:
            List of AlbumSchema objects.
        """
        try:
            new_albums = [
                Album(
                    name=album.name,
                    artist_id=album.artist_id
                )
                for album in albums
            ]

            self.session.add_all(new_albums)
            self.session.commit()

            return AlbumSchema().dump(new_albums, many=True)

        except Exception:
            logging.info("Something happened while creating multiple albums")
            return None

    def get_albums(self):
        """Retrieves all albums.

        Returns:
            List of AlbumSchema objects.
        """
        try:
            albums = self.session.query(Album).all()

            return AlbumSchema().dump(albums, many=True)

        except Exception:
            logging.info("Something happened while retrieving all albums")
            return None

    def get_album_by_id(self, album_id: int) -> Optional[AlbumSchema]:
        """Retrieves an album by its id.

        Args:
            album_id: album unique identifier.

        Returns:
            AlbumSchema object.
        """
        try:
            album = self.session.query(Album).filter(Album.id == album_id).first()

            return AlbumSchema().dump(album)

        except Exception:
            logging.info(f"Something happened while retrieving album with id: {album_id}")
            return None