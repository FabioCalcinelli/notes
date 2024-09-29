from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to use later
db = SQLAlchemy()


def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes import notes_bp
    app.register_blueprint(notes_bp, url_prefix='/notes')

    return app

