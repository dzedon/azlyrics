import logging
from typing import Optional

from domain.song.data import SongData, SongFiltersData
from domain.song.repositories import SongRepository

logger = logging.getLogger("AZ_LYRICS")


class SongService:
    """Songs service."""

    def __init__(self, song_repository: SongRepository):
        """Initializes the service."""
        self.song_repository = song_repository

    def create_multiple_songs(self, songs: list, album_id: int) -> Optional[list[SongData]]:
        """Creates multiple songs registers.

        Args:
            songs: List of SongSchema objects.
            album_id: Album unique identifier.

        Returns:
            List of SongData objects.
        """
        logging.info(f"Creating multiple songs for album with id: {album_id}")
        new_songs = self.song_repository.create_multiple_songs(songs=songs, album_id=album_id)

        return new_songs

    def get_songs(self) -> Optional[list[SongData]]:
        """Retrieves all songs.

        Returns:
            songs: list of SongData objects.
        """
        logging.info("Retrieving all songs.")
        songs = self.song_repository.get_songs()

        return songs

    def get_song_by_id(self, song_id: int) -> SongData:
        """Retrieves a song by its id.

        Args:
            song_id: songs unique identifier.

        Returns:
            song: SongData object.
        """
        logging.info(f"Retrieving song with id: {song_id}")
        song = self.song_repository.get_song_by_id(song_id=song_id)

        if not song:
            message = f"Song with id: {song_id} not found."
            logging.info(message)
            raise Exception(message)

        return song

    def get_songs_filtered(self, filters: SongFiltersData) -> [list[SongData], int]:
        """Retrieves songs filtered by params.

        Args:
            filters: SongFiltersData object with filters and orders.

        Returns:
            songs: List of SongData objects
            count: total number of registers.
        """
        try:
            logging.info(f"Retrieving songs filtered by: {filters}")

            songs, count = self.song_repository.get_songs_filtered(filters=filters)

            return songs, count

        except Exception:
            raise Exception("Something happened while retrieving songs filtered.")
