from marshmallow import Schema, fields, post_load
from domain.artist.data import ArtistData, ArtistFilters
from datetime import datetime

class ArtistSchema(Schema):
    """Schema to serialize and deserialize Artist objects."""
    id = fields.Int(attribute='id')
    url_name = fields.Str(attribute='url_name')
    name = fields.Str(attribute="name")

    @post_load
    def make_artist(self, data, **kwargs):
        return ArtistData(**data)


class ArtistFiltersSchema(Schema):
    # field: Literal["id","url_name","name"] = None
    field = fields.Str(attribute='field')
    operator = fields.Str(attribute='operator')
    value = fields.Str(attribute='value')
    offset = fields.Int(attribute='offset')
    limit = fields.Int(attribute='limit')
    # operator: Literal[
    #    "equals",
    #    "not_equals",
    #    "greater_than",
    #    "less_than",
    #    "less_equals_than",
    #    "greater_equals_than",
    #    "like",
    #    "ilike",
    #    "not_ilike",
    #    "in",
    #    "not_in",
    # ] = None
    # value: Union[str, int] = None

    @post_load
    def make_artist_filters(self, data, **kwargs):
        return ArtistFilters(**data)