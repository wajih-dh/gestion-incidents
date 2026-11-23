import os
from flask import Flask
from . import db, routes


def create_app(config=None):
    app = Flask(__name__)
    app.config["DATABASE"] = os.environ.get("DATABASE", "data/incidents.db")
    if config:
        app.config.update(config)
    os.makedirs(os.path.dirname(app.config["DATABASE"]) or ".", exist_ok=True)
    db.init_app(app)
    app.register_blueprint(routes.bp)
    return app