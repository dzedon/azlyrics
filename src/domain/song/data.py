import inspect

from dataclasses import dataclass
from typing import Union, Literal


@dataclass
class SongData:
    """Song dataclass."""
    name: str
    album_id: int = None
    id: int = None

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass
class SongFiltersData:
    """Song filters dataclass."""
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
    offset: int = 0
    limit: int = 50
