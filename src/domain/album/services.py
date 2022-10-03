import requests
from bs4 import BeautifulSoup
from re import search
from typing import Any

from settings import settings
from domain.album.schemas import AlbumSchema
from domain.album.repositories import AlbumRepository

# TODO: ADD LOGGINS
# TODO: FILL DOCSTRINGS

class AlbumService:

    def __init__(self, album_repository: AlbumRepository):
        self.album_repository = album_repository

    def create_album(self, album: AlbumSchema):
        """***"""
        new_album = self.album_repository.create(album=album)

        return new_album

    def create_multiple_albums(self, albums: list, artist_id: int):
        """Creates multiple albums.

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

        new_albums = self.album_repository.create_multiple_albums(albums=album_list)

        return new_albums

    def get_albums(self):
        """***"""
        albums = self.album_repository.get_albums()

        return albums

    def get_album_by_id(self, album_id: int):
        """***"""
        album = self.album_repository.get_album_by_id(album_id=album_id)

        return album