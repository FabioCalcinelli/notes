from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Create the SQLAlchemy object to use later
db = SQLAlchemy()


import os
def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    import pathlib
    db_path = pathlib.Path(app.config['SQLALCHEMY_DATABASE_URI'].split('sqlite:///')[-1])
    db_path.parent.mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    CORS(app, resources={r"/notes/*": {"origins": "*"}, r"/notes/": {"origins": "*"}})

    from app.routes import notes_bp
    app.register_blueprint(notes_bp, url_prefix='/notes')

    return app

