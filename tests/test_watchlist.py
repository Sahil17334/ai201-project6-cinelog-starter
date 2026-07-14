import pytest
from services.watchlist_service import add_to_watchlist
from services.collection_service import FilmNotFoundError

def test_add_to_watchlist_nonexistent_film_raises(app):
    with pytest.raises(FilmNotFoundError):
        add_to_watchlist(user_id=1, film_id=9999)