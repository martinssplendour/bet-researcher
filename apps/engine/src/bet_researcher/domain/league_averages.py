"""Step 12 of docs/method.md: league scoring averages, blended early in the season."""

import math
from collections.abc import Sequence
from dataclasses import dataclass

from bet_researcher.core.errors import DomainError
from bet_researcher.domain.match_record import MatchRecord

FULL_WEIGHT_ROUNDS = 6


@dataclass(frozen=True, slots=True)
class LeagueAverages:
    """Average goals per game scored by home teams and by away teams."""

    home_goals: float
    away_goals: float

    def __post_init__(self) -> None:
        for value in (self.home_goals, self.away_goals):
            if not math.isfinite(value) or value <= 0:
                raise DomainError("League averages must be finite and above zero.")

    @property
    def per_team_goals(self) -> float:
        """Goals one team scores in an average game, home and away combined."""
        return (self.home_goals + self.away_goals) / 2


def averages_from_matches(matches: Sequence[MatchRecord]) -> LeagueAverages:
    """Plain averages over the given matches."""
    if not matches:
        raise DomainError("League averages need at least one match.")
    count = len(matches)
    return LeagueAverages(
        home_goals=sum(match.home_goals for match in matches) / count,
        away_goals=sum(match.away_goals for match in matches) / count,
    )


def blended_league_averages(
    current: Sequence[MatchRecord],
    previous: Sequence[MatchRecord],
    matches_per_round: int,
    full_weight_rounds: int = FULL_WEIGHT_ROUNDS,
) -> LeagueAverages:
    """This season's averages, blended with last season's until enough rounds are played."""
    if matches_per_round < 1 or full_weight_rounds < 1:
        raise DomainError("Rounds must contain at least one match.")
    if not current and not previous:
        raise DomainError("No league matches to average.")
    if not previous:
        return averages_from_matches(current)
    if not current:
        return averages_from_matches(previous)

    this_season = averages_from_matches(current)
    last_season = averages_from_matches(previous)
    rounds_played = len(current) / matches_per_round
    weight = min(1.0, rounds_played / full_weight_rounds)
    return LeagueAverages(
        home_goals=weight * this_season.home_goals + (1 - weight) * last_season.home_goals,
        away_goals=weight * this_season.away_goals + (1 - weight) * last_season.away_goals,
    )
