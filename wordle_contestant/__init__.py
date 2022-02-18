from flask import Flask

from wordle_contestant.api import api


def create_app():
    """Create Flask app."""

    app = Flask(__name__)
    api.init_app(app)

    return app
