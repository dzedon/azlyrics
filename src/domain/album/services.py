import logging

from domain.album.schemas import AlbumSchema
from domain.album.repositories import AlbumRepository
from domain.album.dataclass import AlbumFilters


logger = logging.getLogger("AZ_LYRICS")

class AlbumService:

    def __init__(self, album_repository: AlbumRepository):
        self.album_repository = album_repository

    def create_album(self, album: AlbumSchema):
        """Creates a new album register.

        Args:
            album: AlbumSchema object.

        Returns:
            AlbumSchema object.
        """
        logging.info(f"Creating album: {album.name}")
        new_album = self.album_repository.create(album=album)

        return new_album

    def create_multiple_albums(self, albums: list, artist_id: int):
        """Creates multiple albums registers.

        Args:
            albums: A list of albums to be created.
            artist_id: The id of the artist to which the albums belong.

        Returns:
            A list of AlbumSchema objects.
        """
        album_list = []
        for album in albums:
            new_album = AlbumSchema()
            new_album.name = album
            new_album.artist_id = artist_id
            album_list.append(new_album)

        logging.info(f"Creating albums for artist with id: {artist_id}")
        new_albums = self.album_repository.create_multiple_albums(albums=album_list)

        return new_albums

    def get_albums(self):
        """Retrieves all albums.

        Returns:
            List of AlbumSchema objects.
        """
        logging.info("Getting all albums")
        albums = self.album_repository.get_albums()

        return albums

    def get_album_by_id(self, album_id: int):
        """Retrieves an album by its id.

        Args:
            album_id: album unique identifier.

        Returns:
            AlbumSchema object.
        """
        logging.info(f"Getting album with id: {album_id}")
        album = self.album_repository.get_album_by_id(album_id=album_id)

        return album

    def get_albums_filtered(self, params: dict):
        """
        Retrieves albums filtered by params.

        Args:
            params: dict with filters and orders.

        Returns:
           ***
        """
        try:
            filters = [AlbumFilters(**filter_) for filter_ in params.get('filters')]

            logging.info(f"Retrieving albums filtered by: {filters}")

            albums, count = self.album_repository.get_albums_filtered(
                filters=filters
            )

            return AlbumSchema().dump(albums, many=True), count

        except Exception:
            raise Exception("Something happened while retrieving albums filtered.")