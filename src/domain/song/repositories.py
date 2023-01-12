import logging
from typing import Optional, List
from datetime import date

from database.filtering import FILTER_MAP
from database.repositories import OrmRepository
from domain.song.data import SongData, SongFiltersData, SongArtistData
from domain.song.models import Song
from domain.album.models import Album
from domain.artist.models import Artist


logger = logging.getLogger("SongRepository")


class SongRepository(OrmRepository):
    """Song repository."""

    def create_multiple_songs(self, songs: list, album_id: int) -> Optional[list[SongData]]:
        """Create multiple songs registers.

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
            logger.exception(
                "Something happened while creating multiple songs for album with id: {album_id}"
            )
            return None

    def get_songs(self) -> Optional[list[SongData]]:
        """Retrieve all songs.

        Returns:
            List of SongData objects.
        """
        try:
            songs = self.session.query(Song).all()

            return [SongData.from_dict(song.__dict__) for song in songs]

        except Exception:
            logger.exception("Something happened while retrieving all songs.")
            return None

    def get_songs_by_artist_id(self, artist_id: int) -> Optional[list[SongArtistData]]:
        """Retrieve a song by its id.

        Args:
            artist_id: songs unique identifier.

        Returns:
            SongData object.
        """
        try:
            results = (
                self.session
                .query(Song, Artist.url_name)
                .select_from(Song)
                .join(Album, Album.id == Song.album_id)
                .join(Artist, Artist.id == Album.artist_id)
                .filter(Album.artist_id == artist_id)
                .all()
            )

            if not results:
                return results

            # TODO: Needs to be refactor, not cool
            songs = []
            for element in results:
                song = SongArtistData.from_dict(element[0].__dict__)
                song.artist_url_name = element[1]
                songs.append(song)

            return songs

        except Exception:
            logger.exception(
                f"Something happened while retrieving songs by artist id: {artist_id}.")
            return None

    def get_song_by_id(self, song_id: int) -> Optional[SongData]:
        """Retrieve a song by its id.

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
            logger.exception(f"Something happened while retrieving song by id: {song_id}.")
            return None

    def get_songs_filtered(self, filters: list[SongFiltersData]) -> [list[SongData], int]:
        """Retrieve songs filtered by params.

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
            logger.exception("Something happened while retrieving songs filtered.")
            return []

    def update_song_by_id(self, song_id: int, song_data: dict) -> Optional[int]:
        """Update a list of songs by its id.

        Args:
            ***
        Returns:
            True
        """
        try:
            logger.info(f"Updating song id: {song_id}.")
            song_data["updated_at"] = date.today()

            self.session.query(Song).filter(Song.id == song_id).update(song_data)

            self.session.commit()

            return True

        except Exception:
            logger.exception("Something happened updating the songs.")
            return False
