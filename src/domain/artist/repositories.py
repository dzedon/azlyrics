from typing import Optional
import logging

from database.repositories import OrmRepository
from domain.artist.models import Artist
from domain.artist.schemas import ArtistSchema

logger = logging.getLogger("AZ_LYRICS")

class ArtistRepository(OrmRepository):

    def create_artist(self, artist: ArtistSchema) -> Optional[ArtistSchema]:
        """Creates a new artist register.

        Args:
            artist: ArtistSchema object.

        Returns:
            ArtistSchema object.
        """
        try:
            new_artist = Artist(
                name=artist.artist_name,
                url_name=artist.url_name
            )

            self.session.add(new_artist)
            self.session.commit()

            return ArtistSchema.dump(new_artist)

        except Exception:
            logging.exception("Something happened while creating artist.")
            return None

    def create_multiple_artists(self, artists: list) -> Optional[list[ArtistSchema]]:
        """Creates multiple artists registers.

        Args:
            artists: List of ArtistSchema objects.

        Returns:
            List of ArtistSchema objects.
        """
        try:
            new_artists = [
                Artist(
                    name=artist.artist_name,
                    url_name=artist.url_name
                )
                for artist in artists
            ]

            self.session.add_all(new_artists)
            self.session.commit()

            return ArtistSchema().dump(new_artists, many=True)

        except Exception:
            logging.info("Something happened while creating multiple artists.")
            return None

    def get_artists(self) -> Optional[list[ArtistSchema]]:
        """Retrieves all artists.

        Returns:
            List of ArtistSchema objects.
        """
        try:
            artists = self.session.query(Artist).all()

            return ArtistSchema().dump(artists, many=True)

        except Exception:
            logging.exception("Something happened while retrieving artists.")
            return []

    def get_artist_by_id(self, artist_id: int) -> Optional[ArtistSchema]:
        """Retrieves an artist by its id.

        Args:
            artist_id: artist's unique identifier.

        Returns:
            ArtistSchema object.
        """
        try:
            artist = self.session.query(Artist).filter_by(id=artist_id).first()

            return ArtistSchema().dump(artist)

        except Exception:
            logging.exception(f"Something happened while retrieving artist by id: {artist_id}.")
            return None
