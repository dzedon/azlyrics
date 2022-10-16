import logging
from re import search

import requests
from bs4 import BeautifulSoup

from domain.album.services import AlbumService
from domain.artist.data import ArtistData
from domain.artist.schemas import ArtistSchema
from domain.artist.services import ArtistService
from domain.song.services import SongService
from settings import settings

logger = logging.getLogger("AZ_LYRICS")


class ScrapperService:
    """Scrapper service."""

    def __init__(
        self, artist_service: ArtistService, album_service: AlbumService, song_service: SongService
    ):
        """Initialize the scrapper service."""
        self.artist_service = artist_service
        self.album_service = album_service
        self.song_service = song_service

    def _get_artists(self, artists_results: list) -> list[ArtistData]:
        """Cleans the artist name.

        Args:
            artists_results: list with all the artists web page data.

        Returns:
            artists_list: list with 5 ArtistData objects.
        """
        logging.info("Filtering artists")

        artist_list = []
        for artist in artists_results:

            url_name = search("(?<=a\/).*?(?=\.html)", artist)  # noqa: W605
            artist_name = search("(?<=>).*?(?=<)", artist)  # noqa: W605

            if url_name and artist_name:

                logger.info("Found an artist.")
                new_artist = ArtistData(url_name=url_name.group(), name=artist_name.group())

                artist_list.append(new_artist)

        return artist_list[:5]

    def _get_artist_albums_and_songs(self, results: list, artist_name: str) -> dict:
        """Filter the artist albums and songs from the web page.

        Args:
            results: web page data.
            artist_name: artist name.

        Returns:
            artist_albums: dictionary with albums and songs.
        """
        logging.info("Filtering artist albums and songs")
        artist_albums = {}
        for line in results:
            album = search('(?<=b>").*?(?="<\/b>)', line)  # noqa: W605
            if album:
                logging.info("Found an album.")
                album_name = album.group()
                artist_albums[album_name] = []
            song = search(f"(?<={artist_name}\/).*?(?=\.html)", line)  # noqa: W605
            if song:
                logging.info("Found a song.")
                artist_albums[album_name].append(song.group())

        return artist_albums

    def _get_artist_albums_and_songs_from_url(self, artist: ArtistSchema) -> list:
        """Retrieves all the artist albums and songs from the web page.

        Args:
            artist: ArtistSchema object.

        Returns:
            list with all the artist's albums and songs.
        """
        logging.info("Retrieving artist albums and songs from url")

        url_name = artist.url_name

        artist_url = settings.azlyrics_artist.format(url_name[0], url_name)
        params = {"q": url_name, "x": settings.azlyrics_x_param}

        url_response = requests.get(url=artist_url, params=params)

        soup = BeautifulSoup(markup=url_response.content, features="html.parser")

        artist_items = soup.find_all(name="div", id="listAlbum")

        return [str(element) for line in artist_items for element in line]

    def _get_artist_from_url(self, artist_letter: str) -> list:
        """Retrieves all the artists from the web page.

        Args:
            artist_letter: The letter to search for artists.

        Returns:
            list with all the artists web page data.
        """
        logging.info("Retrieving artists from url")
        az_url = settings.azlyrics_url.format(artist_letter)

        url_response = requests.get(url=az_url)
        soup = BeautifulSoup(markup=url_response.content, features="html.parser")

        artists_web = soup.find_all(name="div", class_="col-sm-6 text-center artist-col")

        return [str(element) for line in artists_web for element in line]

    def fill_artists(self, artist_letter: str) -> bool:
        """Fill the database with new artists.

        Args:
            artist_letter: The letter to search for artists.

        Returns:
            True if the artists were added to the database.
        """
        try:
            results = self._get_artist_from_url(artist_letter=artist_letter)

            filtered_result = self._get_artists(artists_results=results)

            self.artist_service.create_multiple_artists(artists=filtered_result)

        except Exception:
            logger.exception("Something happened while filling artists.")
            return False

        return True

    def fill_artist_items(self, artist_id: int) -> bool:
        """Fill the database with new albums and songs from an artist.

        Args:
            artist_id: artists unique identifier.

        Returns:
            True
        """
        try:
            artist = self.artist_service.get_artist_by_id(artist_id=artist_id)

            results = self._get_artist_albums_and_songs_from_url(artist=artist)

            artist_albums = self._get_artist_albums_and_songs(
                results=results, artist_name=artist.url_name
            )

            albums = self.album_service.create_multiple_albums(
                albums=artist_albums.keys(), artist_id=artist.id
            )

            if not albums:
                logger.exception("No albums found.")
                raise Exception

            for album in albums:
                album_name = album.name
                album_id = album.id

                self.song_service.create_multiple_songs(
                    songs=artist_albums.get(album_name), album_id=album_id
                )

        except Exception:
            logger.exception("Something happened while filling artist items.")
            return False

        return True
