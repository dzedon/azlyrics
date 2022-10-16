from flask import Blueprint, jsonify, request

from domain.album.schemas import AlbumFiltersSchema, AlbumSchema
from domain.album.services import AlbumService
from utils.dependencies import album_repository

album_blueprint = Blueprint("album", __name__)


@album_blueprint.route("", methods=["GET"])
def get_album():
    """Retrieves all albums."""
    album_service = AlbumService(album_repository=album_repository)

    albums = album_service.get_albums()
    results = [AlbumSchema().dump(album) for album in albums]

    return jsonify({"albums": results})


@album_blueprint.route("/<int:album_id>", methods=["GET"])
def get_album_by_id(album_id: int):
    """Retrieves an album by id."""
    album_service = AlbumService(album_repository=album_repository)

    album = album_service.get_album_by_id(album_id=album_id)
    result = AlbumSchema().dump(album)

    return jsonify({"album": result})


@album_blueprint.route("/search-album", methods=["GET"])
def get_filtered_albums():
    """Retrieves albums filtered by a search term."""
    filters = AlbumFiltersSchema().load(request.args)

    album_service = AlbumService(album_repository)

    albums, count = album_service.get_albums_filtered(filters=filters)

    results = [AlbumSchema().dump(album) for album in albums]

    return jsonify(
        {"songs": results, "count": count, "offset": filters.offset, "limit": filters.limit}
    )
