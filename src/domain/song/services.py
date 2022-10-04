import logging

from domain.song.schemas import SongSchema
from domain.song.repositories import SongRepository

logger = logging.getLogger("AZ_LYRICS")

class SongService:

    def __init__(self, song_repository: SongRepository):
        self.song_repository = song_repository

    def create_song(self, song: SongSchema):
        """Creates a new song register.

        Args:
            song: SongSchema object.

        Returns:
            SongSchema object.
        """
        logging.info(f"Creating song with name: {song.name}")
        new_song = self.song_repository.create_song(song=song)

        return new_song

    def create_multiple_songs(self, songs: list, album_id: int):
        """Creates multiple songs registers.

        Args:
            songs: List of SongSchema objects.

        Returns:
            List of SongSchema objects.
        """
        logging.info(f"Creating multiple songs for album with id: {album_id}")
        new_songs = self.song_repository.create_multiple_songs(songs=songs, album_id=album_id)

        return new_songs

    def get_songs(self):
        """Retrieves all songs.

        Returns:
            songs: list of SongSchema objects.
        """
        logging.info("Retrieving all songs.")
        songs = self.song_repository.get_songs()

        return songs

    def get_song_by_id(self, song_id: int):
        """Retrieves a song by its id.

        Args:
            song_id: songs unique identifier.

        Returns:
            song: SongSchema object.
        """
        logging.info(f"Retrieving song with id: {song_id}")
        song = self.song_repository.get_song_by_id(song_id=song_id)

        return song