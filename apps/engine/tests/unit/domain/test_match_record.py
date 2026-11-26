from collections.abc import Callable
from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from app.core.errors import DomainError
from app.domain.match_record import MatchRecord

pytestmark = pytest.mark.unit

MakeMatch = Callable[..., MatchRecord]


def test_reads_goals_from_the_home_side(make_match: MakeMatch) -> None:
    match = make_match(home=1, away=2, home_goals=3, away_goals=1)

    assert match.goals_for(1) == 3
    assert match.goals_against(1) == 1
    assert match.is_home(1)


def test_reads_goals_from_the_away_side(make_match: MakeMatch) -> None:
    match = make_match(home=1, away=2, home_goals=3, away_goals=1)

    assert match.goals_for(2) == 1
    assert match.goals_against(2) == 3
    assert not match.is_home(2)


def test_involves_only_its_two_teams(make_match: MakeMatch) -> None:
    match = make_match(home=1, away=2)

    assert match.involves(1)
    assert match.involves(2)
    assert not match.involves(3)


def test_rejects_a_team_that_did_not_play(make_match: MakeMatch) -> None:
    match = make_match(home=1, away=2)

    with pytest.raises(DomainError, match="did not play"):
        match.goals_for(99)


def test_rejects_the_same_team_on_both_sides(make_match: MakeMatch) -> None:
    with pytest.raises(DomainError, match="two different teams"):
        make_match(home=5, away=5)


def test_rejects_negative_goals(make_match: MakeMatch) -> None:
    with pytest.raises(DomainError, match="negative"):
        make_match(home_goals=-1)


def test_rejects_kickoff_without_timezone() -> None:
    with pytest.raises(DomainError, match="timezone"):
        MatchRecord(
            fixture_id=1,
            kickoff=datetime(2026, 11, 1, 15, 30),  # noqa: DTZ001 - deliberately naive
            season=2026,
            competition_id=78,
            home_team_id=1,
            away_team_id=2,
            home_goals=1,
            away_goals=0,
        )


def test_is_immutable(make_match: MakeMatch) -> None:
    match = make_match()

    with pytest.raises(FrozenInstanceError):
        match.home_goals = 9  # type: ignore[misc]
