import logging

from domain.artist.schemas import ArtistSchema
from domain.artist.repositories import ArtistRepository
from domain.artist.dataclass import Artist, ArtistFilters

logger = logging.getLogger("AZ_LYRICS")

class ArtistService:

    def __init__(self, artist_repository: ArtistRepository):
        self.artist_repository = artist_repository

    def create_multiple_artists(self, artists: list):
        """Creates a new artist register.

        Args:
            artists: ArtistSchema object.

        Returns:
            ArtistSchema object.
        """
        logging.info("Creating multiple artists.")
        new_artists = self.artist_repository.create_multiple_artists(artists=artists)

        return new_artists

    def get_artists(self):
        """Creates multiple artists registers.

        Returns:
            List of ArtistSchema objects.
        """
        logging.info("Retrieving all artists.")
        artists = self.artist_repository.get_artists()

        return artists

    def get_artist_by_id(self, artist_id: int) -> ArtistSchema:
        """Retrieves an artist by its id.

        Args:
            artist_id: artist's unique identifier.

        Returns:
            artist: ArtistSchema object.
        """
        logging.info(f"Retrieving artist by id: {artist_id}")
        artist = self.artist_repository.get_artist_by_id(artist_id=artist_id)

        return artist

    def get_artists_filtered(self, params: dict):
        """
        Retrieves artists filtered by params.

        Args:
            params: dict with filters and orders.

        Returns:
           ***
        """
        try:
            filters = [ArtistFilters(**filter_) for filter_ in params.get('filters')]

            logging.info(f"Retrieving artists filtered by: {filters}")

            artists, count = self.artist_repository.get_artists_filtered(
                filters=filters
            )

            return ArtistSchema().dump(artists, many=True), count

        except Exception:
            raise Exception("Something happened while retrieving artists filtered.")
