from flask_restful import Api

api = Api()


class FlaskRestfulApi:

    def __init__(self, app):
        api.init_app(app)


def api_route(path):
    """
    Decorator for registering API endpoints.
    """

    class WrappedClass:
        def __init__(self, cls):
            api.add_resource(cls, path)
    return WrappedClass
