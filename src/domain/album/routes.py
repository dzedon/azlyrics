from flask import Blueprint, jsonify

from domain.album.services import AlbumService
from domain.album.repositories import AlbumRepository
from utils.dependencies import album_repository

albums = Blueprint('album', __name__)


@albums.route('', methods=['GET'])
def get_album():
    """Get all albums."""

    album_service = AlbumService(album_repository=album_repository)

    albums = album_service.get_albums()

    return jsonify({'albums': albums})

@albums.route('/<int:album_id>', methods=['GET'])
def get_album_by_id(album_id: int):
    """Get album by id."""

    album_service = AlbumService(album_repository=album_repository)

    album = album_service.get_album_by_id(album_id=album_id)

    return jsonify({'album': album})

