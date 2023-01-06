import inspect
from dataclasses import dataclass, field
from typing import Literal, Union


@dataclass(kw_only=True)
class SongData:
    """Song dataclass."""

    name: str
    album_id: int = None
    id: int = None
    lyrics: str = None

    @classmethod
    def from_dict(cls, env):
        """Creates a SongData object from a dictionary."""
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})


@dataclass(kw_only=True)
class SongArtistData(SongData):
    """Song with artist_url_name dataclass."""

    artist_url_name: str = None


@dataclass
class SongFiltersData:
    """Song filters dataclass."""

    field: Literal["id", "album_id", "name", "lyrics"] = None
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
