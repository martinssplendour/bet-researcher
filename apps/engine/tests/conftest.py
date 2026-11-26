"""Shared test fixtures."""

from collections.abc import Callable, Iterator
from datetime import UTC, datetime, timedelta

import pytest

from app.domain.match_record import MatchRecord

BASE_KICKOFF = datetime(2026, 11, 1, 15, 30, tzinfo=UTC)


@pytest.fixture
def make_match() -> Callable[..., MatchRecord]:
    """Build finished matches with sensible defaults; override any field by keyword."""
    ids: Iterator[int] = iter(range(1, 100_000))

    def _make(
        *,
        home: int = 1,
        away: int = 2,
        home_goals: int = 1,
        away_goals: int = 1,
        days_ago: int = 7,
        season: int = 2026,
        competition: int = 78,
        fixture_id: int | None = None,
    ) -> MatchRecord:
        return MatchRecord(
            fixture_id=fixture_id if fixture_id is not None else next(ids),
            kickoff=BASE_KICKOFF - timedelta(days=days_ago),
            season=season,
            competition_id=competition,
            home_team_id=home,
            away_team_id=away,
            home_goals=home_goals,
            away_goals=away_goals,
        )

    return _make
