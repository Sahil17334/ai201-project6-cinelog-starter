import pytest
from tests.test_collection import app
from services.watchlist_service import add_to_watchlist
from services.collection_service import FilmNotFoundError

def test_add_to_watchlist_nonexistent_film_raises(app):
    with pytest.raises(FilmNotFoundError):
        add_to_watchlist(user_id="user-1", film_id="123e4567-e89b-12d3-a456-426614174000")