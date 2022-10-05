from flask import Blueprint, jsonify, request

from domain.song.services import SongService
from utils.dependencies import song_repository

song_blueprint = Blueprint('song', __name__)


@song_blueprint.route('/', methods=['GET'])
def get_song():
    """Retrieves all songs."""

    song_service = SongService(song_repository)

    songs = song_service.get_songs()

    return jsonify({'songs': songs})


@song_blueprint.route('/<int:song_id>', methods=['GET'])
def get_song_by_id(song_id):
    """Retrieves a song by its id."""

    song_service = SongService(song_repository)

    song = song_service.get_song_by_id(song_id)

    return jsonify({'song': song})


@song_blueprint.route('/search-song', methods=['POST'])
def get_filtered_songs():
    """Retrieves songs filtered by a search term."""

    song_service = SongService(song_repository)

    songs, count = song_service.get_songs_filtered(params=request.get_json())

    return jsonify({'songs': songs, 'count': count})
