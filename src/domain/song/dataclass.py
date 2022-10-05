from dataclasses import dataclass
from typing import Union, Literal


@dataclass
class SongFilters:
    field: Literal[
        "id",
        "album_id",
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
