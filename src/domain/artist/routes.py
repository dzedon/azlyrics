import logging

from flask import Blueprint, jsonify, request

from domain.album.services import AlbumService
from domain.artist.schemas import ArtistFiltersSchema, ArtistSchema
from domain.artist.services import ArtistService
from domain.song.services import SongService
from helper.scrapper.services import ScrapperService
from utils.dependencies import album_repository, artist_repository, song_repository
from settings import settings
artist_blueprint = Blueprint("artist", __name__)

logger = logging.getLogger("ArtistRouter")

@artist_blueprint.route("/fill-database", methods=["POST"])
def fill_artists():
    f"""Fill db with {settings.ARTISTS_MAX_LIMIT} artists."""

    payload = request.get_json()

    logger.info(f"Filling artist for letter: {payload}.")

    artist_service = ArtistService(artist_repository=artist_repository)
    album_service = AlbumService(album_repository=album_repository)
    song_service = SongService(song_repository=song_repository)

    scrapper_service = ScrapperService(
        artist_service=artist_service, album_service=album_service, song_service=song_service
    )

    scrapper_service.fill_artists(artist_letter=payload.get("search_letter"))

    return jsonify({"database": "db filled"})


@artist_blueprint.route("/<int:artist_id>/fill-database", methods=["POST"])
def fill_artist_items(artist_id):
    f"""Fill db with {settings.ALBUMS_MAX_LIMIT} artist's albums and {settings.SONGS_MAX_LIMIT} songs per 
    album."""
    artist_service = ArtistService(artist_repository=artist_repository)
    album_service = AlbumService(album_repository=album_repository)
    song_service = SongService(song_repository=song_repository)

    scrapper_service = ScrapperService(
        artist_service=artist_service, album_service=album_service, song_service=song_service
    )

    scrapper_service.fill_artist_items(artist_id=artist_id)

    return jsonify({"database": "db filled"})


@artist_blueprint.route("/<int:artist_id>/fill-lyrics", methods=["POST"])
def fill_artist_lyrics(artist_id):
    """Fill artist's songs with their lyrics."""
    logger.info(f"Filling lyrics for artist id: {artist_id}")
    artist_service = ArtistService(artist_repository=artist_repository)
    album_service = AlbumService(album_repository=album_repository)
    song_service = SongService(song_repository=song_repository)

    scrapper_service = ScrapperService(
        artist_service=artist_service, album_service=album_service, song_service=song_service
    )

    songs = scrapper_service.fill_artist_lyrics(artist_id=artist_id)

    return jsonify({"cool": songs})


@artist_blueprint.route("", methods=["GET"])
def get_artists():
    """Retrieve all artists in the database."""
    logger.info("Retrieving all artists.")
    artists_service = ArtistService(artist_repository=artist_repository)

    artists = artists_service.get_artists()
    results = [ArtistSchema().dump(artist) for artist in artists]

    return jsonify({"artist": results})


@artist_blueprint.route("/<int:artist_id>", methods=["GET"])
def get_artist_by_id(artist_id):
    """Retrieve an artist by its id."""
    logger.info(f"Retrieving artist by id: {artist_id}")
    artists_service = ArtistService(artist_repository=artist_repository)

    artist = artists_service.get_artist_by_id(artist_id=artist_id)
    result = ArtistSchema().dump(artist)

    return jsonify({"artist": result})


@artist_blueprint.route("/search-artist", methods=["GET"])
def get_filtered_artists():
    """Retrieve artists filtered by a search field."""
    filters = ArtistFiltersSchema().load(request.args)
    logger.info(f"Retrieving artists filtered by: {filters}")

    artists_service = ArtistService(artist_repository=artist_repository)

    artists, count = artists_service.get_artists_filtered(filters=filters)

    results = [ArtistSchema().dump(artist) for artist in artists]

    return jsonify(
        {"artists": results, "count": count, "offset": filters.offset, "limit": filters.limit}
    )
