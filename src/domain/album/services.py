import logging
from typing import Optional
from domain.album.schemas import AlbumSchema
from domain.album.repositories import AlbumRepository
from domain.album.data import AlbumFiltersData, AlbumData


logger = logging.getLogger("AZ_LYRICS")

class AlbumService:

    def __init__(self, album_repository: AlbumRepository):
        self.album_repository = album_repository

    def create_multiple_albums(self, albums: list, artist_id: int) -> Optional[list[AlbumData]]:
        """Creates multiple albums registers.

        Args:
            albums: A list of albums to be created.
            artist_id: The id of the artist to which the albums belong.

        Returns:
            A list of AlbumData objects.
        """
        logging.info(f"Creating albums for artist with id: {artist_id}")
        new_albums = self.album_repository.create_multiple_albums(albums=albums, artist_id=artist_id)

        return new_albums

    def get_albums(self) -> Optional[list[AlbumData]]:
        """Retrieves all albums.

        Returns:
            List of AlbumData objects.
        """
        logging.info("Getting all albums")
        albums = self.album_repository.get_albums()

        return albums

    def get_album_by_id(self, album_id: int) -> Optional[AlbumData]:
        """Retrieves an album by its id.

        Args:
            album_id: album unique identifier.

        Returns:
            AlbumSchema object.
        """
        logging.info(f"Getting album with id: {album_id}")
        album = self.album_repository.get_album_by_id(album_id=album_id)

        if not album:
            message = f"Song with id: {album_id} not found."
            logging.info(message)
            raise Exception(message)

        return album

    def get_albums_filtered(self, filters: AlbumFiltersData) -> [list[AlbumData], int]:
        """
        Retrieves albums filtered by params.

        Args:
            filters: AlbumFiltersData object with filters and orders.

        Returns:
            albums: List of AlbumData objects
            count: total number of registers.
        """
        try:

            logging.info(f"Retrieving albums filtered by: {filters}")

            albums, count = self.album_repository.get_albums_filtered(
                filters=filters
            )

            return albums, count

        except Exception:
            raise Exception("Something happened while retrieving albums filtered.")