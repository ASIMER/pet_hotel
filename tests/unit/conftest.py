import pytest

from pet_hotel import create_app


@pytest.fixture
def app():
    app = create_app()
    with app.test_client() as client:
        return client
