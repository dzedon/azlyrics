from domain.song.schemas import SongSchema
from domain.song.repositories import SongRepository

# TODO: ADD LOGGER

class SongService:

    def __init__(self, song_repository: SongRepository):
        self.song_repository = song_repository

    def create_song(self, song: SongSchema):
        """Creates a new song."""
        new_song = self.song_repository.create_song(song=song)

        return new_song

    def create_multiple_songs(self, songs: list, album_id: int):
        """Creates multiple songs."""
        new_songs = self.song_repository.create_multiple_songs(songs=songs, album_id=album_id)

        return new_songs

    def get_songs(self):
        """Retrieves all songs.

        Returns:
            songs: list of SongSchema objects.
        """
        songs = self.song_repository.get_songs()

        return songs

    def get_song_by_id(self, song_id: int):
        """Retrieves a song by its id.

        Args:
            song_id: songs unique identifier.

        Returns:
            song: SongSchema object.
        """
        song = self.song_repository.get_song_by_id(song_id=song_id)

        return song