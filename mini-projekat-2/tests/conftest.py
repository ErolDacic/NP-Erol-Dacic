import pytest


@pytest.fixture
def sample_rows():
    return [
        {"reservation_id": "1", "guest": "Ana", "nights": 2,
         "price_per_night": "100", "discount_percent": "10", "status": "potvrdjena"},
        {"reservation_id": "2", "guest": "Milo", "nights": 1,
         "price_per_night": "50", "discount_percent": "0", "status": "otkazana"},
    ]
