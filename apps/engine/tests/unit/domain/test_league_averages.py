from collections.abc import Callable

import pytest

from app.core.errors import DomainError
from app.domain.league_averages import (
    LeagueAverages,
    averages_from_matches,
    blended_league_averages,
)
from app.domain.match_record import MatchRecord

pytestmark = pytest.mark.unit

MakeMatch = Callable[..., MatchRecord]
MATCHES_PER_ROUND = 9


def test_averages_home_and_away_goals(make_match: MakeMatch) -> None:
    matches = [make_match(home_goals=2, away_goals=1), make_match(home_goals=1, away_goals=1)]

    averages = averages_from_matches(matches)

    assert averages.home_goals == pytest.approx(1.5)
    assert averages.away_goals == pytest.approx(1.0)
    assert averages.per_team_goals == pytest.approx(1.25)


def test_averages_need_at_least_one_match() -> None:
    with pytest.raises(DomainError, match="at least one match"):
        averages_from_matches([])


@pytest.mark.parametrize(("home", "away"), [(0.0, 1.0), (1.0, 0.0), (-1.0, 1.0)])
def test_rejects_non_positive_averages(home: float, away: float) -> None:
    with pytest.raises(DomainError):
        LeagueAverages(home_goals=home, away_goals=away)


def test_after_six_rounds_only_this_season_counts(make_match: MakeMatch) -> None:
    current = [make_match(home_goals=2, away_goals=1) for _ in range(6 * MATCHES_PER_ROUND)]
    previous = [make_match(home_goals=1, away_goals=1) for _ in range(10)]

    blended = blended_league_averages(current, previous, matches_per_round=MATCHES_PER_ROUND)

    assert blended.home_goals == pytest.approx(2.0)
    assert blended.away_goals == pytest.approx(1.0)


def test_early_season_blends_in_last_season(make_match: MakeMatch) -> None:
    current = [make_match(home_goals=3, away_goals=1) for _ in range(MATCHES_PER_ROUND)]
    previous = [make_match(home_goals=1, away_goals=1) for _ in range(10)]

    blended = blended_league_averages(current, previous, matches_per_round=MATCHES_PER_ROUND)

    # One round played: weight 1/6 on this season, 5/6 on last season.
    assert blended.home_goals == pytest.approx(3 / 6 + 5 / 6)
    assert blended.away_goals == pytest.approx(1.0)


def test_uses_whichever_season_exists(make_match: MakeMatch) -> None:
    only = [make_match(home_goals=2, away_goals=2)]

    assert blended_league_averages(only, [], MATCHES_PER_ROUND).home_goals == pytest.approx(2.0)
    assert blended_league_averages([], only, MATCHES_PER_ROUND).away_goals == pytest.approx(2.0)


def test_blend_needs_some_matches() -> None:
    with pytest.raises(DomainError):
        blended_league_averages([], [], MATCHES_PER_ROUND)


def test_blend_rejects_invalid_round_size(make_match: MakeMatch) -> None:
    with pytest.raises(DomainError):
        blended_league_averages([make_match()], [], matches_per_round=0)
