from datetime import datetime

from flask import Flask, jsonify

from domain.album.routes import album_blueprint
from domain.artist.routes import artist_blueprint
from domain.song.routes import song_blueprint
from settings import settings

app = Flask(__name__)
app.register_blueprint(blueprint=artist_blueprint, url_prefix="/artist")
app.register_blueprint(blueprint=album_blueprint, url_prefix="/album")
app.register_blueprint(blueprint=song_blueprint, url_prefix="/song")


@app.route("/")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.now()})


if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug)
