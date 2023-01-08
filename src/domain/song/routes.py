from flask import Blueprint, jsonify, request

from domain.song.schemas import SongFiltersSchema, SongSchema
from domain.song.services import SongService
from utils.dependencies import song_repository

song_blueprint = Blueprint("song", __name__)


@song_blueprint.route("/", methods=["GET"])
def get_song():
    """Retrieve all songs."""
    song_service = SongService(song_repository)

    songs = song_service.get_songs()
    results = [SongSchema().dump(song) for song in songs]

    return jsonify({"songs": results})


@song_blueprint.route("/<int:song_id>", methods=["GET"])
def get_song_by_id(song_id):
    """Retrieve a song by its id."""
    song_service = SongService(song_repository)

    song = song_service.get_song_by_id(song_id)
    result = SongSchema().dump(song)

    return jsonify({"song": result})


@song_blueprint.route("/search-song", methods=["GET"])
def get_filtered_songs():
    """Retrieve songs filtered by a search field."""
    filters = SongFiltersSchema().load(request.args)

    song_service = SongService(song_repository)

    songs, count = song_service.get_songs_filtered(filters=filters)

    results = [SongSchema().dump(song) for song in songs]

    return jsonify(
        {"songs": results, "count": count, "offset": filters.offset, "limit": filters.limit}
    )
