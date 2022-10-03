from database.repositories import OrmRepository
from domain.song.models import Song
from domain.song.schemas import SongSchema
from typing import Optional

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
            return None

    def create_multiple_songs(self, songs: list, album_id: int) -> Optional[list[SongSchema]]:
        """Creates multiple songs.

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
            return None