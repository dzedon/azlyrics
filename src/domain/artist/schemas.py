from marshmallow import Schema, fields


class ArtistSchema(Schema):
    """Schema to serialize and deserialize Artist objects."""
    id: int = fields.Int(attribute='id')
    url_name: str = fields.Str(attribute='url_name')
    artist_name: str = fields.Str(attribute="name")
