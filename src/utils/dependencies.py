from database.session import session
from domain.artist.repositories import ArtistRepository
from domain.album.repositories import AlbumRepository
from domain.song.repositories import SongRepository

artist_repository = ArtistRepository(session=next(session()))
album_repository = AlbumRepository(session=next(session()))
song_repository = SongRepository(session=next(session()))