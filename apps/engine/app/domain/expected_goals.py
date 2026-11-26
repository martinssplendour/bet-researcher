"""Steps 16 and 44 of docs/method.md: baseline expected goals and the capped AI adjustment."""

import math
from dataclasses import dataclass

from app.core.errors import DomainError
from app.domain.league_averages import LeagueAverages
from app.domain.team_ratings import TeamRating

DEFAULT_ADJUSTMENT_FLOOR = 0.7
DEFAULT_ADJUSTMENT_CEILING = 1.3


@dataclass(frozen=True, slots=True)
class ExpectedGoals:
    """Goals each side is expected to score in the match."""

    home: float
    away: float

    def __post_init__(self) -> None:
        for value in (self.home, self.away):
            if not math.isfinite(value) or value < 0:
                raise DomainError("Expected goals must be finite and not negative.")


@dataclass(frozen=True, slots=True)
class AdjustmentBounds:
    """Limits on how far the AI analyst may move a team's expected goals."""

    floor: float = DEFAULT_ADJUSTMENT_FLOOR
    ceiling: float = DEFAULT_ADJUSTMENT_CEILING

    def __post_init__(self) -> None:
        if not 0.0 < self.floor <= 1.0 <= self.ceiling:
            raise DomainError("Adjustment bounds must satisfy 0 < floor <= 1 <= ceiling.")

    def clamp(self, multiplier: float) -> float:
        """Keep a multiplier inside the bounds."""
        if not math.isfinite(multiplier) or multiplier <= 0:
            raise DomainError("An adjustment multiplier must be a positive, finite number.")
        return min(self.ceiling, max(self.floor, multiplier))


DEFAULT_ADJUSTMENT_BOUNDS = AdjustmentBounds()


def baseline_expected_goals(
    home: TeamRating, away: TeamRating, league: LeagueAverages
) -> ExpectedGoals:
    """League average x own attack x opponent's defence, for each side."""
    return ExpectedGoals(
        home=league.home_goals * home.attack * away.defence,
        away=league.away_goals * away.attack * home.defence,
    )


def apply_adjustment(
    base: ExpectedGoals,
    home_multiplier: float,
    away_multiplier: float,
    bounds: AdjustmentBounds = DEFAULT_ADJUSTMENT_BOUNDS,
) -> ExpectedGoals:
    """Apply the analyst's multipliers, capped by `bounds` whatever the analyst asked for."""
    return ExpectedGoals(
        home=base.home * bounds.clamp(home_multiplier),
        away=base.away * bounds.clamp(away_multiplier),
    )
