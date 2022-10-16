from marshmallow import Schema, fields, post_load
from domain.album.data import AlbumData, AlbumFiltersData


class AlbumSchema(Schema):
    """Schema to serialize and deserialize Album objects."""
    id: int = fields.Int(attribute='id')
    name: str = fields.Str(attribute='name')
    artist_id: int = fields.Int(attribute="artist_id")

    @post_load
    def make_album(self, data, **kwargs):
        return AlbumData(**data)


class AlbumFiltersSchema(Schema):
    """Schema to serialize and deserialize Album objects."""
    field = fields.Str(attribute='field')
    operator = fields.Str(attribute='operator')
    value = fields.Str(attribute='value')
    offset = fields.Int(attribute='offset')
    limit = fields.Int(attribute='limit')

    @post_load
    def make_album_filters(self, data, **kwargs):
        return AlbumFiltersData(**data)