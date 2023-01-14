import logging
from re import search
from typing import Any, List
from time import sleep

import requests
from bs4 import BeautifulSoup

from domain.album.services import AlbumService
from domain.artist.data import ArtistData
from domain.artist.services import ArtistService
from domain.song.services import SongService
from settings import settings

logger = logging.getLogger("ScrapperService")


class ScrapperService:
    """Scrapper service."""

    def __init__(
        self, artist_service: ArtistService, album_service: AlbumService, song_service: SongService
    ):
        """Initialize the scrapper service."""
        self.artist_service = artist_service
        self.album_service = album_service
        self.song_service = song_service

    def _albums_and_songs_generator(self, results: List) -> Any:
        """Generator for the albums and songs URL response.

        Args:
            results: list with all the albums and songs web page data.

        Yields:
            ArtistSchema object.
        """
        for element in results:
            yield element

    def _artist_generator(self, artists_results: list) -> ArtistData:
        """Generator for the artists URL response.

        Args:
            artists_results: list with all the artists web page data.

        Yields:
            ArtistData object.
        """
        # TODO: Chech Single Responsability Principle
        for artist in artists_results:

            url_name = search("(?<=a\/).*?(?=\.html)", artist)  # noqa: W605
            artist_name = search("(?<=>).*?(?=<)", artist)  # noqa: W605

            if url_name and artist_name:
                url_name = url_name.group()
                artist_name = artist_name.group()

                logger.info(f"Found artist {artist_name}.")

                yield ArtistData(url_name=url_name, name=artist_name)

    def _filter_artists(self, artists_results: list) -> list[ArtistData]:
        """Clean the artist name.

        Args:
            artists_results: list with all the artists web page data.

        Returns:
            artists_list: list with 5 ArtistData objects.
        """
        logger.info("Filtering artists")
        artists_list = []

        # TODO: replace this with itertools module
        for artist in self._artist_generator(artists_results=artists_results):
            artists_list.append(artist)

            if len(artists_list) == settings.ARTISTS_MAX_LIMIT:
                logger.info(f"Found {settings.ARTISTS_MAX_LIMIT} artists.")
                return artists_list

    def _filter_artist_albums_and_songs(self, results: list, artist_name: str) -> dict:
        """Filter the artist albums and songs from the web page.

        Args:
            results: web page data.
            artist_name: artist name.

        Returns:
            artist_albums: dictionary with albums and songs.
        """
        logger.info("Filtering artist albums and songs")

        artist_albums = {}
        album_name = ""
        for line in self._albums_and_songs_generator(results=results):

            album = search('(?<=b>").*?(?="<\/b>)', line)  # noqa: W605
            if album:
                logger.info("Found an album.")
                album_name = album.group()
                artist_albums[album_name] = []

            if len(artist_albums.get(album_name, ".")) == settings.SONGS_MAX_LIMIT:
                logger.info(f"Album has {settings.SONGS_MAX_LIMIT} songs.")

                if len(artist_albums) == settings.ALBUMS_MAX_LIMIT:
                    logger.info(f"Artist has {settings.ALBUMS_MAX_LIMIT} albums.")
                    return artist_albums

                continue

            song = search(f"(?<={artist_name}\/).*?(?=\.html)", line)  # noqa: W605
            if song:
                logger.info("Found a song.")
                artist_albums.get(album_name).append(song.group())

        return artist_albums

    def _get_artist_albums_and_songs_from_url(self, artist: ArtistData) -> list:
        """Retrieve all the artist albums and songs from the web page.

        Args:
            artist: ArtistSchema object.

        Returns:
            list with all the artist's albums and songs.
        """
        logger.info("Retrieving artist albums and songs from url")

        url_name = artist.url_name

        artist_url = settings.AZLYRICS_ARTIST.format(url_name[0], url_name)
        params = {"q": url_name, "x": settings.AZLYRICS_X_PARAM}

        url_response = requests.get(url=artist_url, params=params)

        soup = BeautifulSoup(markup=url_response.content, features="html.parser")

        artist_items = soup.find_all(name="div", id="listAlbum")

        return [str(element) for line in artist_items for element in line]

    def _get_artist_from_url(self, artist_letter: str) -> list:
        """Retrieve all the artists from the web page.

        Args:
            artist_letter: The letter to search for artists.

        Returns:
            list with all the artists web page data.
        """
        logger.info("Retrieving artists from url")
        az_url = settings.AZLYRICS_URL.format(artist_letter)

        url_response = requests.get(url=az_url)
        
        soup = BeautifulSoup(markup=url_response.content, features="html.parser")

        artists_web = soup.find_all(name="div", class_="col-sm-6 text-center artist-col")

        return [str(element) for line in artists_web for element in line]

    def _filter_lyrics(self, results: list) -> str:
        """Filter URL results to only leave the song lyrics.

        Args:
            results: results.

        Returns:
            Complete lyric as a string.
        """
        results = [res for res in results if res.startswith('\n')]

        return "".join(results)

    def _get_lyrics_from_url(self, song_name: str, artist_name: str):
        """***."""
        # TODO: needs to be refactored.
        logger.info(f"Constructing URL for song: {song_name} from artist: {artist_name}.")
        az_url = f'{settings.AZLYRICS_URL}/{artist_name}/{song_name}.html'.format('lyrics')

        logger.info(f"Calling URL: {az_url}")
        url_response = requests.get(url=az_url)

        if url_response.status_code != 200:
            logger.info(f"Something wrong with URL, status code: {url_response.status_code}")
            return None

        logger.info("Scrapping HTML.")
        soup = BeautifulSoup(markup=url_response.content, features="html.parser")

        song_lyrics = soup.find_all(name="div", class_="")

        if not song_lyrics:
            logger.info("Scrapped HTML failed.")
            return None

        logger.info("HTML scrapped successfully.")
        return [str(element) for line in song_lyrics for element in line]

    def _remove_multiple_songs_from_songs_list(self, songs: list) -> list:
        """***."""
        # TODO: TEMP.
        logger.info("Removing multiple records.")
        old_album_id = 0
        song_counter = 0
        new_song_list = []

        for song in songs:
            if song.album_id != old_album_id:
                old_album_id = song.album_id
                song_counter = 0

            if song.lyrics or song_counter == settings.ALBUM_SONGS_MAX_LIMIT:
                continue

            new_song_list.append(song)
            song_counter += 1

        return new_song_list

    def fill_artists(self, artist_letter: str) -> bool:
        """Fill the database with new artists.

        Args:
            artist_letter: The letter to search for artists.

        Returns:
            True if the artists were added to the database.
        """
        try:
            results = self._get_artist_from_url(artist_letter=artist_letter)

            filtered_result = self._filter_artists(artists_results=results)

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

            artist_albums = self._filter_artist_albums_and_songs(
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

    def fill_artist_lyrics(self, artist_id: int):
        """Fill the database with new albums and songs from an artist.

        Args:
            artist_id: artists unique identifier.

        Returns:
            True
        """
        try:
            songs_list = self.song_service.get_songs_by_artist_id(artist_id=artist_id)

            songs = self._remove_multiple_songs_from_songs_list(songs=songs_list)

            # TODO: refactor
            for song in songs:
                results = self._get_lyrics_from_url(
                    song_name=song.name, artist_name=song.artist_url_name)
                song.lyrics = self._filter_lyrics(results=results)
                self.song_service.update_song_by_id(song_id=song.id, song_data={
                    "lyrics": song.lyrics})
                sleep(settings.SLEEP_TIMEOUT)

        except Exception:
            logger.exception(
                f"Something happened while filling artist with id: {artist_id} lyrics.")
            return False

        logger.info(f"Artist id: {artist_id} lyrics filled.")
        return True
