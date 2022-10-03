from database.repositories import OrmRepository
from domain.album.models import Album
from domain.album.schemas import AlbumSchema
from typing import Optional

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
                name=album.album_name,
                artist_id=album.artist_id
            )

            self.session.add(new_album)
            self.session.commit()

            return AlbumSchema.dump(new_album)

        except Exception:
            return None

    def create_multiple_albums(self, albums: list) -> Optional[list[AlbumSchema]]:
        """Creates multiple album.

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
            return None