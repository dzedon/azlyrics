from flask import Blueprint, jsonify

from domain.song.services import SongService
from utils.dependencies import song_repository

songs = Blueprint('song', __name__)


@songs.route('/', methods=['GET'])
def get_song():
    """Retrieves all songs."""

    song_service = SongService(song_repository)

    songs = song_service.get_songs()

    return jsonify({'songs': songs})


@songs.route('/<int:song_id>', methods=['GET'])
def get_song_by_id(song_id):
    """Retrieves a song by its id."""

    song_service = SongService(song_repository)

    song = song_service.get_song_by_id(song_id)

    return jsonify({'song': song})