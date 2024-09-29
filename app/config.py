class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/notes.db'  # Default for development
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory for testing
    TESTING = True
