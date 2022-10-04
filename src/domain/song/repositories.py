import logging
from typing import Optional

from database.repositories import OrmRepository
from domain.song.models import Song
from domain.song.schemas import SongSchema


logger = logging.getLogger("AZ_LYRICS")

class SongRepository(OrmRepository):

    def create_song(self, song: SongSchema) -> Optional[SongSchema]:
        """Creates a new song register.

        Args:
            song: SongSchema object.

        Returns:
            SongSchema object.
        """
        try:
            new_song = Song(
                name=song.song_name,
                album_id=song.album_id,
                artist_id=song.artist_id
            )

            self.session.add(new_song)
            self.session.commit()

            return SongSchema.dump(new_song)

        except Exception:
            logging.exception("Something happened while creating song.")
            return None

    def create_multiple_songs(self, songs: list, album_id: int) -> Optional[list[SongSchema]]:
        """Creates multiple songs registers.

        Args:
            songs: List of SongSchema objects.

        Returns:
            List of SongSchema objects.
        """
        try:
            new_songs = [
                Song(
                    name=song,
                    album_id=album_id,
                )
                for song in songs
            ]

            self.session.add_all(new_songs)
            self.session.commit()

            return SongSchema().dump(new_songs, many=True)

        except Exception:
            logging.exception("Something happened while creating multiple songs for album with id: {album_id}")
            return None

    def get_songs(self) -> Optional[list[SongSchema]]:
        """Retrieves all songs.

        Returns:
            List of SongSchema objects.
        """
        try:
            songs = self.session.query(Song).all()

            return SongSchema().dump(songs, many=True)

        except Exception:
            logging.exception("Something happened while retrieving all songs.")
            return None

    def get_song_by_id(self, song_id: int) -> Optional[SongSchema]:
        """Retrieves a song by its id.

        Args:
            song_id: songs unique identifier.

        Returns:
            SongSchema object.
        """
        try:
            song = self.session.query(Song).filter_by(id=song_id).first()

            return SongSchema().dump(song)

        except Exception:
            logging.exception(f"Something happened while retrieving song by id: {song_id}.")
            return None