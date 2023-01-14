import logging

logging.basicConfig(level=logging.INFO)


class Settings:
    """Main Settings class."""

    # project settings
    host: str = "0.0.0.0"
    port: int = 5001
    debug: bool = True

    # database
    DATABASE_URI: str = "postgresql://user:password@lyrics_db/lyric"

    # azlyrics
    AZLYRICS_URL: str = "https://www.azlyrics.com/{}.html"
    # AZLYRICS_URL: str = "https://www.azlyrics.com/lyrics"
    AZLYRICS_ARTIST: str = "https://www.azlyrics.com/{}/{}.html"
    AZLYRICS_SEARCH: str = "https://search.azlyrics.com/search.php"
    AZLYRICS_X_PARAM: str = "f103343153744bb15c416120f86dcb61cf2ab2ef9a7b3fe3b241e29f957bfcb1"
    ALBUMS_MAX_LIMIT: int = 5
    ALBUM_SONGS_MAX_LIMIT: int = 2
    SONGS_MAX_LIMIT: int = 5
    ARTISTS_MAX_LIMIT: int = 5
    SLEEP_TIMEOUT: int = 20


settings = Settings()
