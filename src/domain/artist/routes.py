from flask import Blueprint, jsonify, request

from helper.scrapper.services import ScrapperService
from domain.artist.services import ArtistService
from domain.album.services import AlbumService
from domain.song.services import SongService
from utils.dependencies import artist_repository, album_repository, song_repository

artist_blueprint = Blueprint('artist', __name__)


@artist_blueprint.route('/fill-database', methods=['POST'])
def fill_artists():
    """Fill db with 5 artists."""

    payload = request.get_json()

    artist_service = ArtistService(artist_repository=artist_repository)
    album_service = AlbumService(album_repository=album_repository)
    song_service = SongService(song_repository=song_repository)

    scrapper_service = ScrapperService(
        artist_service=artist_service, album_service=album_service, song_service=song_service
    )

    scrapper_service.fill_artists(artist_letter=payload.get('search_letter'))

    return jsonify({'database': "db filled"})


@artist_blueprint.route('/<int:artist_id>/fill-database', methods=['POST'])
def fill_artist_items(artist_id):
    """Fill db with artist's albums and songs"""

    artist_service = ArtistService(artist_repository=artist_repository)
    album_service = AlbumService(album_repository=album_repository)
    song_service = SongService(song_repository=song_repository)

    scrapper_service = ScrapperService(
        artist_service=artist_service, album_service=album_service, song_service=song_service
    )

    scrapper_service.fill_artist_items(artist_id=artist_id)

    return jsonify({'database': "db filled"})


@artist_blueprint.route('', methods=['GET'])
def get_artists():
    """Retrieves all artists in the database."""

    artists_service = ArtistService(artist_repository=artist_repository)

    artists = artists_service.get_artists()

    return jsonify({'artist': artists})


@artist_blueprint.route('/<int:artist_id>', methods=['GET'])
def get_artist_by_id(artist_id):
    """Retrieves an artist by its id."""

    artists_service = ArtistService(artist_repository=artist_repository)

    artist = artists_service.get_artist_by_id(artist_id=artist_id)

    return jsonify({'artist': artist})


@artist_blueprint.route('/search-artist', methods=['GET'])
def get_filtered_artists():
    """Retrieves artists filtered by a search term."""

    # TODO: add pagination and filtering

    payload = request.get_json()
    offset = payload.get('offset')
    limit = payload.get('limit')

    artists_service = ArtistService(artist_repository=artist_repository)

    raise NotImplementedError
