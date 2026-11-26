import math

import pytest

from bet_researcher.core.errors import DomainError
from bet_researcher.domain.expected_goals import (
    AdjustmentBounds,
    ExpectedGoals,
    apply_adjustment,
    baseline_expected_goals,
)
from bet_researcher.domain.league_averages import LeagueAverages
from bet_researcher.domain.team_ratings import TeamRating

pytestmark = pytest.mark.unit

BASE = ExpectedGoals(home=2.6, away=0.9)


def test_baseline_combines_attack_defence_and_league_averages() -> None:
    league = LeagueAverages(home_goals=1.6, away_goals=1.2)
    home = TeamRating(attack=1.88, defence=0.83, weighted_games=12.0)
    away = TeamRating(attack=0.92, defence=0.88, weighted_games=12.0)

    expected = baseline_expected_goals(home=home, away=away, league=league)

    assert expected.home == pytest.approx(1.6 * 1.88 * 0.88)
    assert expected.away == pytest.approx(1.2 * 0.92 * 0.83)


def test_adjustment_multiplies_each_side() -> None:
    adjusted = apply_adjustment(BASE, home_multiplier=0.8, away_multiplier=1.0)

    assert adjusted.home == pytest.approx(2.08)
    assert adjusted.away == pytest.approx(0.9)
    assert ExpectedGoals(home=2.6, away=0.9) == BASE


def test_adjustment_is_capped_at_thirty_percent() -> None:
    adjusted = apply_adjustment(BASE, home_multiplier=0.2, away_multiplier=2.0)

    assert adjusted.home == pytest.approx(2.6 * 0.7)
    assert adjusted.away == pytest.approx(0.9 * 1.3)


def test_custom_bounds() -> None:
    bounds = AdjustmentBounds(floor=0.9, ceiling=1.1)

    adjusted = apply_adjustment(BASE, home_multiplier=0.5, away_multiplier=1.5, bounds=bounds)

    assert adjusted.home == pytest.approx(2.6 * 0.9)
    assert adjusted.away == pytest.approx(0.9 * 1.1)


@pytest.mark.parametrize("multiplier", [0.0, -1.0, math.nan, math.inf])
def test_rejects_invalid_multipliers(multiplier: float) -> None:
    with pytest.raises(DomainError):
        apply_adjustment(BASE, home_multiplier=multiplier, away_multiplier=1.0)


@pytest.mark.parametrize(("floor", "ceiling"), [(1.2, 1.3), (0.7, 0.9), (0.0, 1.3)])
def test_bounds_must_straddle_no_change(floor: float, ceiling: float) -> None:
    with pytest.raises(DomainError):
        AdjustmentBounds(floor=floor, ceiling=ceiling)


@pytest.mark.parametrize(("home", "away"), [(-0.1, 1.0), (1.0, math.nan), (math.inf, 1.0)])
def test_expected_goals_must_be_finite_and_non_negative(home: float, away: float) -> None:
    with pytest.raises(DomainError):
        ExpectedGoals(home=home, away=away)
