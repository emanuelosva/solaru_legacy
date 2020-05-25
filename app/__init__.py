"""App Factory."""

# Flask
from flask import Flask
from flask_bootstrap import Bootstrap

# Settings
from .config import config
settings_module = config.ProductionConfig


def app_factory():

    # App factory
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(settings_module)

    return app
