import os

class Settings:
    """Main Settings class."""

    # project settings
    host: str = "0.0.0.0"
    port: str = 5001
    debug: bool = True

    # database
    database_uri: str = "postgresql://user:password@lyrics_db/lyric"

    # azlyrics
    azlyrics_url: str = "https://www.azlyrics.com/{}.html"
    azlyrics_artist: str = "https://www.azlyrics.com/{}/{}.html"
    azlyrics_search: str = "https://search.azlyrics.com/search.php"
    azlyrics_x_param: str = "f103343153744bb15c416120f86dcb61cf2ab2ef9a7b3fe3b241e29f957bfcb1"


settings = Settings()
