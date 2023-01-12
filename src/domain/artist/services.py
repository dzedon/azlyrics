import logging
from typing import Optional

from domain.artist.data import ArtistData, ArtistFiltersData
from domain.artist.repositories import ArtistRepository

logger = logging.getLogger("ArtistService")


class ArtistService:
    """Artists service."""

    def __init__(self, artist_repository: ArtistRepository):
        """Initializes Artists service."""
        self.artist_repository = artist_repository

    def create_multiple_artists(self, artists: list) -> Optional[list[ArtistData]]:
        """Create a new artist register.

        Args:
            artists: ArtistSchema object.

        Returns:
            ArtistSchema object.
        """
        logger.info("Creating multiple artists.")
        new_artists = self.artist_repository.create_multiple_artists(artists=artists)

        return new_artists

    def get_artists(self) -> [Optional[ArtistData]]:
        """Retrieve multiple artists registers.

        Returns:
            artists: List of ArtistData objects.
        """
        logger.info("Retrieving all artists.")
        artists = self.artist_repository.get_artists()

        return artists

    def get_artist_by_id(self, artist_id: int) -> Optional[ArtistData]:
        """Retrieve an artist by its id.

        Args:
            artist_id: artist's unique identifier.

        Returns:
            ArtistData object.
        """
        logger.info(f"Retrieving artist by id: {artist_id}")
        artist = self.artist_repository.get_artist_by_id(artist_id=artist_id)

        if not artist:
            message = f"Artist with id: {artist_id} not found."
            logger.info(message)
            raise Exception(message)

        return artist

    def get_artists_filtered(self, filters: ArtistFiltersData) -> [ArtistData, int]:
        """Retrieve artists filtered by params.

        Args:
            filters: ArtistFiltersData object with filters and orders.

        Returns:
            artists: List of ArtistData objects
            count: total number of registers.
        """
        try:
            logger.info(f"Retrieving artists filtered by: {filters}")

            artists, count = self.artist_repository.get_artists_filtered(filters=filters)

            return artists, count

        except Exception:
            raise Exception("Something happened while retrieving artists filtered.")
