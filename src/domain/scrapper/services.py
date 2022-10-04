import logging
from re import search
from typing import Any

from bs4 import BeautifulSoup
import requests

from settings import settings
from domain.artist.services import ArtistService
from domain.artist.schemas import ArtistSchema
from domain.album.services import AlbumService
from domain.song.services import SongService


logger = logging.getLogger("AZ_LYRICS")


class ScrapperService:

    def __init__(self, artist_service: ArtistService, album_service: AlbumService, song_service: SongService):
        self.artist_service = artist_service
        self.album_service = album_service
        self.song_service = song_service

    def _artist_generator(self, artists_results: Any) -> ArtistSchema:
        """***"""
        for element in artists_results:
            for artist in element:
                artist = str(artist)
                url_name = search("(?<=a\/).*?(?=\.html)", artist)
                artist_name = search("(?<=>).*?(?=<)", artist)
                if url_name and artist_name:
                    new_artist = ArtistSchema()
                    new_artist.url_name = url_name.group()
                    new_artist.artist_name = artist_name.group()
                    yield new_artist

    def _filter_results(self, artists_results: Any) -> list:
        """Cleans the artist name.

        Args:
            ***

        Returns:
            ***
        """
        artist = self._artist_generator(artists_results=artists_results)

        artist_list = []

        for _ in range(50):
            artist_list.append(next(artist))
            if len(artist_list) == 10:
                return artist_list

    def _get_artist_albums_and_songs(self, results: list, artist_name: str) -> dict:
        """***"""
        artist_albums = {}
        # TODO: REFACTOR THIS
        for x in results:
            for y in x:
                line = str(y)
                album = search('(?<=b>").*?(?="<\/b>)', line)
                if album:
                    album_name = album.group()
                    artist_albums[album_name] = []
                song = search(f"(?<={artist_name}\/).*?(?=\.html)", line)
                if song:
                    artist_albums[album_name].append(song.group())
        return artist_albums

    def _retrieve_artist_albums_and_songs_from_url(self, artist: ArtistSchema):
        """***"""
        url_name = artist.get('url_name')

        artist_url = settings.azlyrics_artist.format(url_name[0], url_name)
        params = {'q': url_name, "x": settings.azlyrics_x_param}

        url_response = requests.get(url=artist_url, params=params)

        soup = BeautifulSoup(markup=url_response.content, features='html.parser')

        return  soup.find_all(name="div", id="listAlbum")

    def _retrieve_artist_from_url(self, artist_letter: str) -> Any:
        """***"""
        az_url = settings.azlyrics_url.format(artist_letter)

        url_response = requests.get(url=az_url)
        soup = BeautifulSoup(markup=url_response.content, features='html.parser')

        return soup.find_all(name="div", class_="col-sm-6 text-center artist-col")

    def fill_artists(self, artist_letter: str):
        """Fill the database with new artists.

        Args:
            artist_letter: The letter to search for artists.

        Returns:
            artists: List of ArtistSchema objects.
        """
        logging.info("Retrieving artists from url")
        results = self._retrieve_artist_from_url(artist_letter=artist_letter)

        logging.info("Filtering artists")
        filtered_result = self._filter_results(artists_results=results)

        artists = self.artist_service.create_multiple_artists(artists=filtered_result)

        return artists

    def fill_artist_items(self, artist_id: int):
        """***"""
        artist = self.artist_service.get_artist_by_id(artist_id=artist_id)

        logging.info("Retrieving artist albums and songs from url")
        results = self._retrieve_artist_albums_and_songs_from_url(artist=artist)

        logging.info("Filtering artist albums and songs")
        artist_albums = self._get_artist_albums_and_songs(
            results=results, artist_name=artist.get('url_name')
        )

        albums = self.album_service.create_multiple_albums(
            albums=artist_albums.keys(), artist_id=artist.get('id')
        )

        for album in albums:
            album_name = album.get('name')
            album_id = album.get('id')
            artist_songs = self.song_service.create_multiple_songs(
                songs=artist_albums.get(album_name), album_id=album_id
            )

        return artist