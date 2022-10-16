from marshmallow import Schema, fields, post_load
from domain.song.data import SongData, SongFiltersData


class SongSchema(Schema):
    """Schema to serialize and deserialize Song objects."""
    id: int = fields.Int(attribute='id')
    name: str = fields.Str(attribute='name')
    album_id: int = fields.Int(attribute="album_id")

    @post_load
    def make_artist(self, data, **kwargs):
        return SongData(**data)


class SongFiltersSchema(Schema):
    """Schema to serialize and deserialize Song objects."""
    field = fields.Str(attribute='field')
    operator = fields.Str(attribute='operator')
    value = fields.Str(attribute='value')
    offset = fields.Int(attribute='offset')
    limit = fields.Int(attribute='limit')

    @post_load
    def make_song_filters(self, data, **kwargs):
        return SongFiltersData(**data)