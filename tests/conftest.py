import pytest
from app import create_app, db

@pytest.fixture
def app():
    # Use TestConfig for testing
    app = create_app(config_class='app.config.TestConfig')

    # Create tables in the test context
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Create a test client using the Flask app
    return app.test_client()

@pytest.fixture
def runner(app):
    # Create a test runner for CLI commands
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Ensure the app context is active for database operations
        yield db

