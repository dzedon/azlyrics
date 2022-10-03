import requests
from bs4 import BeautifulSoup
from re import search
from typing import Any
import logging

from settings import settings
from domain.artist.schemas import ArtistSchema
from domain.artist.repositories import ArtistRepository

logger = logging.getLogger("AZ_LYRICS")

class ArtistService:

    def __init__(self, artist_repository: ArtistRepository):
        self.artist_repository = artist_repository

    def create_multiple_artists(self, artists: list):
        """***"""
        new_artists = self.artist_repository.create_multiple_artists(artists=artists)

        return new_artists

    def get_artists(self):
        """Retrieves all artists in the database.

        Returns:
            List of ArtistSchema objects.
        """

        artists = self.artist_repository.get_artists()

        return artists

    def get_artist_by_id(self, artist_id: int) -> ArtistSchema:
        """Retrieves an artist by its id.

        Args:
            artist_id: artist's unique identifier.

        Returns:
            artist: ArtistSchema object.
        """
        artist = self.artist_repository.get_artist_by_id(artist_id=artist_id)

        return artist

    def get_albums_and_songs(self):
        pass
