from collections.abc import Callable

import pytest

from bet_researcher.core.errors import DomainError
from bet_researcher.domain.history_window import WeightedMatch, WindowTier
from bet_researcher.domain.league_averages import LeagueAverages
from bet_researcher.domain.match_record import MatchRecord
from bet_researcher.domain.team_ratings import rate_team

pytestmark = pytest.mark.unit

MakeMatch = Callable[..., MatchRecord]
LEAGUE = LeagueAverages(home_goals=1.6, away_goals=1.2)  # 1.4 goals per team per game


def _weighted(match: MatchRecord, weight: float = 1.0) -> WeightedMatch:
    return WeightedMatch(
        match=match, tier=WindowTier.CURRENT_SEASON_THIS_COMPETITION, weight=weight
    )


def test_strong_team_rates_above_average_after_shrinkage(make_match: MakeMatch) -> None:
    window = [_weighted(make_match(home_goals=3, away_goals=1)) for _ in range(10)]

    rating = rate_team(window, team_id=1, league=LEAGUE, shrinkage_games=5.0)

    # Raw attack 3 / 1.4; pulled toward 1.0 by 5 phantom average games.
    assert rating.attack == pytest.approx((10 * 3 / 1.4 + 5) / 15)
    assert rating.defence == pytest.approx((10 * 1 / 1.4 + 5) / 15)
    assert rating.weighted_games == pytest.approx(10.0)


def test_weights_shape_the_averages(make_match: MakeMatch) -> None:
    window = [
        _weighted(make_match(home_goals=4, away_goals=0), weight=1.0),
        _weighted(make_match(home_goals=1, away_goals=2), weight=0.5),
    ]

    rating = rate_team(window, team_id=1, league=LEAGUE, shrinkage_games=0.0)

    assert rating.attack == pytest.approx(3.0 / 1.4)
    assert rating.defence == pytest.approx((1.0 / 1.5) / 1.4)


def test_reads_goals_from_the_teams_own_side(make_match: MakeMatch) -> None:
    window = [_weighted(make_match(home=2, away=1, home_goals=0, away_goals=2))]

    rating = rate_team(window, team_id=1, league=LEAGUE, shrinkage_games=0.0)

    assert rating.attack == pytest.approx(2 / 1.4)
    assert rating.defence == pytest.approx(0.0)


def test_no_history_means_an_average_team() -> None:
    rating = rate_team([], team_id=1, league=LEAGUE)

    assert (rating.attack, rating.defence, rating.weighted_games) == (1.0, 1.0, 0.0)


def test_rejects_negative_shrinkage(make_match: MakeMatch) -> None:
    with pytest.raises(DomainError):
        rate_team([_weighted(make_match())], team_id=1, league=LEAGUE, shrinkage_games=-1.0)
