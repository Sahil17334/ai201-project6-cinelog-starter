# PR Response Doc — CineLog Watchlist Feature

## AI Usage
* Used AI as a pair-programmer to walk through the exact syntax required to implement the deduplication check using SQLAlchemy's `filter_by` and to construct the pytest fixture for testing the `FilmNotFoundError`.

## Comment 1 — Rename
**What I did:** Renamed `save_to_watchlist` to `add_to_watchlist` in `services/watchlist_service.py` and updated the call site in the routes file.
**How I verified:** Ran the test suite to ensure no import errors or undefined functions were triggered.

## Comment 2 — Deduplication
**What I did:** Added a query using `WatchlistEntry.query.filter_by(user_id=user_id, film_id=film_id).first()` inside `add_to_watchlist`. If a record exists, it returns early instead of duplicating.
**How I verified:** Reviewed the parallel logic in `collection_service.py` to ensure the pattern matched exactly.

## Comment 3 — Missing test
**What I did:** Created `tests/test_watchlist.py` and added `test_add_to_watchlist_nonexistent_film_raises`.
**How I verified:** Ran `pytest tests/test_watchlist.py -v` to confirm the test passes and successfully catches the expected `FilmNotFoundError`.

## Comment 4 — Default visibility
**My position:** I am keeping `public=True` as the default.
**Reasoning:** CineLog is fundamentally a social discovery platform. A watchlist is high-value data for future social features (e.g., "Friends want to watch"). Defaulting to public removes friction for the social graph.
**Tradeoff acknowledged:** This prioritizes network effects over strict user privacy. Users who expect private lists by default might accidentally expose their watchlists.

## Comment 5 — Sort order
**My position:** I am changing the default sort order to date-added (descending).
**Reasoning:** I agree with the maintainer's logic. A watchlist acts as an intent-queue. Users are most likely looking for the film they *just* added to watch tonight, making alphabetical sorting frustrating for large lists.
**Engagement with reviewer's point:** The sibling collection feature uses date-added because of the "recently watched" use case; applying the same logic to a "recently wanted to watch" list keeps the platform's UX consistent.

## Comment 6 — Rebase
**What conflicted:** The `film_id` type changed from Integer to UUID/String in `models.py` and `tests/test_watchlist.py` during the rebase.
**How I resolved it:** Updated the database model and test inputs to accept strings instead of integers.
**How I verified no conflict remains:** Re-ran `pytest tests/ -v` to ensure all tests passed against the new UUID types.

## PR Description
**What the feature does:** Adds a watchlist feature allowing users to queue films for future viewing, complete with a `WatchlistEntry` model, deduplication logic, and REST endpoints.
**Design decisions:** Defaults to `public=True` to heavily bias toward future social/discovery features, and sorts by date-added to prioritize recent intent. 
**How to manually test:** Start the app with `python app.py`. Use curl to POST to `/watchlist/<user_id>/add` with a valid `film_id` payload, then GET `/watchlist/<user_id>` to verify the film appears in the list.