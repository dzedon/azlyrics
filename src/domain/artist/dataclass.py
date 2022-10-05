from dataclasses import dataclass
from typing import Union, Literal


@dataclass
class Artist:
    """Artist dataclass."""
    id: int
    url_name: str
    artist_name: str


@dataclass
class ArtistFilters:
    field: Literal[
        "id",
        "url_name",
        "name"
    ] = None
    operator: Literal[
        "equals",
        "not_equals",
        "greater_than",
        "less_than",
        "less_equals_than",
        "greater_equals_than",
        "like",
        "ilike",
        "not_ilike",
        "in",
        "not_in",
    ] = None
    value: Union[str, int] = None
