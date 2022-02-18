from functools import wraps

from flask import request, Response
from flask_restful import Api, Resource
from werkzeug.exceptions import Unauthorized

from wordle_contestant import config
from wordle_contestant.game import run_game

api = Api()


def check_apikey(func):
    """Check API key."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            raise Unauthorized("Missing API key")

        if api_key != config.API_KEY:
            raise Unauthorized("API key mismatch")

        return func(*args, **kwargs)
    return decorated_function


@api.resource("/")
class Index(Resource):

    def get(self, **kwargs):
        """
        Check app availability.
        """

        return Response("Your app is up and running!", 200)

    @check_apikey
    def post(self, **kwargs):
        """
        Check app availability and API key.
        """

        return Response("Success", 200)


@api.resource("/games")
class Games(Resource):

    @check_apikey
    def post(self, **kwargs):
        """
        Run game.
        """

        data = request.get_json(force=True)
        wordle_id = data["wordle_id"]

        run_game(wordle_id)

        return Response("Success", 200)
