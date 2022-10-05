from flask import Blueprint, jsonify, request

from domain.album.services import AlbumService
from utils.dependencies import album_repository

album_blueprint = Blueprint('album', __name__)


@album_blueprint.route('', methods=['GET'])
def get_album():
    """Get all albums."""

    album_service = AlbumService(album_repository=album_repository)

    albums = album_service.get_albums()

    return jsonify({'albums': albums})


@album_blueprint.route('/<int:album_id>', methods=['GET'])
def get_album_by_id(album_id: int):
    """Get album by id."""

    album_service = AlbumService(album_repository=album_repository)

    album = album_service.get_album_by_id(album_id=album_id)

    return jsonify({'album': album})


@album_blueprint.route('/search-album', methods=['POST'])
def get_filtered_albums():
    """Retrieves albums filtered by a search term."""

    album_service = AlbumService(album_repository)

    albums, count = album_service.get_albums_filtered(params=request.get_json())

    return jsonify({'albums': albums, 'count': count})

