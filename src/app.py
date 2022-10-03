
from flask import Flask, jsonify

from datetime import datetime

from domain.artist.routes import artist_blueprint
from domain.album.routes import albums
from domain.song.routes import songs
from settings import settings


app = Flask(__name__)
app.register_blueprint(blueprint=artist_blueprint, url_prefix='/artist')
app.register_blueprint(blueprint=albums, url_prefix='/album')
app.register_blueprint(blueprint=songs, url_prefix='/song')


@app.route('/')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now()})


if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug)