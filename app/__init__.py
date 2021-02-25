from flask import Flask

from app.config import Config
from hello import world


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(world.bp)

    return app
