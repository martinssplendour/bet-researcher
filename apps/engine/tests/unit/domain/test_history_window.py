from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import pytest

from bet_researcher.core.errors import DomainError
from bet_researcher.domain.history_window import (
    WindowConfig,
    WindowRequest,
    WindowTier,
    select_history_window,
)
from bet_researcher.domain.match_record import MatchRecord

pytestmark = pytest.mark.unit

MakeMatch = Callable[..., MatchRecord]

TEAM = 1
LEAGUE = 78
CUP = 81
LOWER_LEAGUE = 79
KICKOFF = datetime(2026, 11, 1, 15, 30, tzinfo=UTC)


def _request(**overrides: Any) -> WindowRequest:
    values: dict[str, Any] = {
        "team_id": TEAM,
        "competition_id": LEAGUE,
        "season": 2026,
        "before": KICKOFF,
    }
    return WindowRequest(**{**values, **overrides})


def test_mid_season_uses_the_last_12_league_games(make_match: MakeMatch) -> None:
    league = [make_match(days_ago=day) for day in range(1, 15)]
    cup = [make_match(competition=CUP, days_ago=day) for day in range(20, 23)]

    window = select_history_window([*cup, *league], _request())

    assert len(window) == 12
    assert {entry.tier for entry in window} == {WindowTier.CURRENT_SEASON_THIS_COMPETITION}
    assert all(entry.weight == 1.0 for entry in window)
    assert [entry.match for entry in window] == league[:12]


def test_fills_from_other_competitions_then_last_season(make_match: MakeMatch) -> None:
    league = [make_match(days_ago=day) for day in range(1, 5)]
    cup = [make_match(competition=CUP, days_ago=day) for day in range(5, 8)]
    last_season = [make_match(season=2025, days_ago=day) for day in range(200, 210)]

    window = select_history_window([*last_season, *cup, *league], _request())

    assert [entry.tier for entry in window] == (
        [WindowTier.CURRENT_SEASON_THIS_COMPETITION] * 4
        + [WindowTier.CURRENT_SEASON_OTHER_COMPETITION] * 3
        + [WindowTier.PREVIOUS_SEASON] * 5
    )
    assert [entry.weight for entry in window] == [1.0] * 4 + [0.7] * 3 + [0.5] * 5
    assert [entry.match for entry in window[7:]] == last_season[:5]


def test_ignores_future_matches_and_other_teams(make_match: MakeMatch) -> None:
    played = make_match(days_ago=3)
    future = make_match(days_ago=-2)
    others = make_match(home=3, away=4, days_ago=4)

    window = select_history_window([played, future, others], _request())

    assert [entry.match for entry in window] == [played]


def test_ignores_older_seasons_and_last_seasons_other_competitions(
    make_match: MakeMatch,
) -> None:
    two_seasons_ago = make_match(season=2024, days_ago=500)
    last_season_cup = make_match(season=2025, competition=CUP, days_ago=250)

    window = select_history_window([two_seasons_ago, last_season_cup], _request())

    assert window == ()


def test_promoted_team_uses_last_seasons_lower_league_at_reduced_weight(
    make_match: MakeMatch,
) -> None:
    lower_league = [
        make_match(season=2025, competition=LOWER_LEAGUE, days_ago=day) for day in range(200, 203)
    ]

    window = select_history_window(
        lower_league,
        _request(is_promoted=True, previous_season_competition_id=LOWER_LEAGUE),
    )

    assert len(window) == 3
    assert all(entry.tier is WindowTier.PREVIOUS_SEASON for entry in window)
    assert all(entry.weight == 0.3 for entry in window)


def test_short_history_returns_what_exists(make_match: MakeMatch) -> None:
    matches = [make_match(days_ago=day) for day in range(1, 4)]

    assert len(select_history_window(matches, _request())) == 3


def test_repeated_fixtures_count_once(make_match: MakeMatch) -> None:
    match = make_match(fixture_id=42, days_ago=2)

    window = select_history_window([match, match], _request())

    assert len(window) == 1


def test_window_size_is_configurable(make_match: MakeMatch) -> None:
    matches = [make_match(days_ago=day) for day in range(1, 10)]

    window = select_history_window(matches, _request(), WindowConfig(size=5))

    assert len(window) == 5


def test_request_rejects_kickoff_without_timezone() -> None:
    with pytest.raises(DomainError, match="timezone"):
        _request(before=datetime(2026, 11, 1, 15, 30))  # noqa: DTZ001 - deliberately naive


@pytest.mark.parametrize(
    "overrides",
    [
        {"size": 0},
        {"current_season_this_competition_weight": 0.0},
        {"previous_season_weight": 1.5},
        {"promoted_previous_season_weight": -0.1},
    ],
)
def test_window_config_rejects_bad_values(overrides: dict[str, Any]) -> None:
    with pytest.raises(DomainError):
        WindowConfig(**overrides)
