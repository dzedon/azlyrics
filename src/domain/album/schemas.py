from marshmallow import Schema, fields


class AlbumSchema(Schema):
    """Schema to serialize and deserialize Album objects."""
    id: int = fields.Int(attribute='id')
    name: str = fields.Str(attribute='name')
    # url_name: str = fields.Str(attribute='url_name')
    artist_id: int = fields.Int(attribute="artist_id")
