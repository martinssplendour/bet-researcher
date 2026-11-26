"""Steps 13-15 of docs/method.md: attack and defence ratings with small-sample protection."""

from collections.abc import Sequence
from dataclasses import dataclass

from app.core.errors import DomainError
from app.domain.history_window import WeightedMatch
from app.domain.league_averages import LeagueAverages

DEFAULT_SHRINKAGE_GAMES = 5.0
AVERAGE_RATING = 1.0


@dataclass(frozen=True, slots=True)
class TeamRating:
    """Attack above 1.0 scores more than average. Defence above 1.0 concedes more (weaker)."""

    attack: float
    defence: float
    weighted_games: float


def rate_team(
    window: Sequence[WeightedMatch],
    team_id: int,
    league: LeagueAverages,
    shrinkage_games: float = DEFAULT_SHRINKAGE_GAMES,
) -> TeamRating:
    """Rate a team from its weighted window, relative to the league average."""
    if shrinkage_games < 0:
        raise DomainError("Shrinkage cannot be negative.")
    total_weight = sum(entry.weight for entry in window)
    if total_weight <= 0:
        return TeamRating(attack=AVERAGE_RATING, defence=AVERAGE_RATING, weighted_games=0.0)

    scored = sum(entry.weight * entry.match.goals_for(team_id) for entry in window) / total_weight
    conceded = (
        sum(entry.weight * entry.match.goals_against(team_id) for entry in window) / total_weight
    )
    return TeamRating(
        attack=_shrink(scored / league.per_team_goals, total_weight, shrinkage_games),
        defence=_shrink(conceded / league.per_team_goals, total_weight, shrinkage_games),
        weighted_games=total_weight,
    )


def _shrink(raw_rating: float, games: float, shrinkage_games: float) -> float:
    """(games x raw + k x average) / (games + k): few games pull the rating toward average."""
    return (games * raw_rating + shrinkage_games * AVERAGE_RATING) / (games + shrinkage_games)
