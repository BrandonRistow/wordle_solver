from flask import Flask

from wordle_contestant.resources import FlaskRestfulApi


def create_app():
    """Create Flask app."""

    app = Flask(__name__)
    FlaskRestfulApi(app)

    return app
