import logging
from typing import Optional

from database.filtering import FILTER_MAP
from database.repositories import OrmRepository
from domain.song.data import SongData, SongFiltersData
from domain.song.models import Song

logger = logging.getLogger("AZ_LYRICS")


class SongRepository(OrmRepository):
    """Song repository."""

    def create_multiple_songs(self, songs: list, album_id: int) -> Optional[list[SongData]]:
        """Creates multiple songs registers.

        Args:
            songs: List of SongData objects.
            album_id: Album unique identifier.

        Returns:
            List of SongData objects.
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

            return new_songs

        except Exception:
            logging.exception(
                "Something happened while creating multiple songs for album with id: {album_id}"
            )
            return None

    def get_songs(self) -> Optional[list[SongData]]:
        """Retrieves all songs.

        Returns:
            List of SongData objects.
        """
        try:
            songs = self.session.query(Song).all()

            return [SongData.from_dict(song.__dict__) for song in songs]

        except Exception:
            logging.exception("Something happened while retrieving all songs.")
            return None

    def get_song_by_id(self, song_id: int) -> Optional[SongData]:
        """Retrieves a song by its id.

        Args:
            song_id: songs unique identifier.

        Returns:
            SongData object.
        """
        try:
            song = self.session.query(Song).filter_by(id=song_id).first()

            if not song:
                return song

            return SongData.from_dict(song.__dict__)

        except Exception:
            logging.exception(f"Something happened while retrieving song by id: {song_id}.")
            return None

    def get_songs_filtered(self, filters: list[SongFiltersData]) -> [list[SongData], int]:
        """Retrieves songs filtered by params.

        Args:
            filters: ArtistFilters object.

        Returns:
            artists: List of ArtistData objects
            count: total number of registers.
        """
        try:
            query = self.session.query(Song)

            if filters.field:
                operator = FILTER_MAP.get(filters.operator)
                field = getattr(Song, filters.field)

                query = operator(query=query, field=field, value=filters.value)

            songs = query.offset(filters.offset).limit(filters.limit).all()

            song_count = query.count()

            songs = [SongData.from_dict(song.__dict__) for song in songs]

            return songs, song_count

        except Exception:
            logging.exception("Something happened while retrieving songs filtered.")
            return []
