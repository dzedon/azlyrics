from marshmallow import Schema, fields


class SongSchema(Schema):
    """Schema to serialize and deserialize Song objects."""
    id: int = fields.Int(attribute='id')
    name: str = fields.Str(attribute='name')
    # url_name: str = fields.Str(attribute='url_name')
    album_id: int = fields.Int(attribute="album_id")