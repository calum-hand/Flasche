import os

from flask import Flask


def create_app() -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    from flasche.blueprints import home, insertion, metrics, quiz, vocabulary

    blueprint_modules = [home, insertion, metrics, quiz, vocabulary]

    for module in blueprint_modules:
        app.register_blueprint(module.bp)

    return app
