from marshmallow import Schema, fields

@dataclass
class Artist:
    """Artist dataclass."""
    id: int
    url_name: str
    artist_name: str
