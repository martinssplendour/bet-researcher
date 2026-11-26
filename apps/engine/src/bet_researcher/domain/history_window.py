"""Steps 10-11 of docs/method.md: pick each team's most relevant recent matches.

Matches are taken newest first from three tiers, in priority order:

1. this season, this competition
2. this season, other competitions
3. last season, this competition (last season's lower league for a promoted team)
"""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum

from bet_researcher.core.errors import DomainError
from bet_researcher.domain.match_record import MatchRecord, require_timezone

DEFAULT_WINDOW_SIZE = 12


class WindowTier(IntEnum):
    """Priority tier of a match in the window. Lower is more relevant."""

    CURRENT_SEASON_THIS_COMPETITION = 1
    CURRENT_SEASON_OTHER_COMPETITION = 2
    PREVIOUS_SEASON = 3


@dataclass(frozen=True, slots=True)
class WindowConfig:
    """Tunable window settings."""

    size: int = DEFAULT_WINDOW_SIZE
    current_season_this_competition_weight: float = 1.0
    current_season_other_competition_weight: float = 0.7
    previous_season_weight: float = 0.5
    promoted_previous_season_weight: float = 0.3

    def __post_init__(self) -> None:
        if self.size < 1:
            raise DomainError("The history window needs room for at least one match.")
        weights = (
            self.current_season_this_competition_weight,
            self.current_season_other_competition_weight,
            self.previous_season_weight,
            self.promoted_previous_season_weight,
        )
        if any(not 0.0 < weight <= 1.0 for weight in weights):
            raise DomainError("Window weights must be above 0 and at most 1.")

    def weight_for(self, tier: WindowTier, *, is_promoted: bool) -> float:
        """Weight a match in this tier carries in the team's averages."""
        if tier is WindowTier.CURRENT_SEASON_THIS_COMPETITION:
            return self.current_season_this_competition_weight
        if tier is WindowTier.CURRENT_SEASON_OTHER_COMPETITION:
            return self.current_season_other_competition_weight
        if is_promoted:
            return self.promoted_previous_season_weight
        return self.previous_season_weight


DEFAULT_WINDOW_CONFIG = WindowConfig()


@dataclass(frozen=True, slots=True)
class WindowRequest:
    """Whose window to build, and for which match."""

    team_id: int
    competition_id: int
    season: int
    before: datetime
    previous_season_competition_id: int | None = None
    is_promoted: bool = False

    def __post_init__(self) -> None:
        require_timezone(self.before, "The window's cut-off time")

    @property
    def last_season_competition_id(self) -> int:
        """Competition whose games count from last season."""
        if self.previous_season_competition_id is None:
            return self.competition_id
        return self.previous_season_competition_id


@dataclass(frozen=True, slots=True)
class WeightedMatch:
    """A match in a team's window, with its tier and weight."""

    match: MatchRecord
    tier: WindowTier
    weight: float


def select_history_window(
    matches: Iterable[MatchRecord],
    request: WindowRequest,
    config: WindowConfig = DEFAULT_WINDOW_CONFIG,
) -> tuple[WeightedMatch, ...]:
    """Return up to `config.size` matches: best tier first, newest first within a tier."""
    unique = {match.fixture_id: match for match in matches}.values()
    candidates = [
        (tier, match)
        for match in unique
        if match.involves(request.team_id) and match.kickoff < request.before
        if (tier := _classify(match, request)) is not None
    ]
    ranked = sorted(candidates, key=lambda item: (item[0], -item[1].kickoff.timestamp()))
    return tuple(
        WeightedMatch(
            match=match,
            tier=tier,
            weight=config.weight_for(tier, is_promoted=request.is_promoted),
        )
        for tier, match in ranked[: config.size]
    )


def _classify(match: MatchRecord, request: WindowRequest) -> WindowTier | None:
    if match.season == request.season:
        if match.competition_id == request.competition_id:
            return WindowTier.CURRENT_SEASON_THIS_COMPETITION
        return WindowTier.CURRENT_SEASON_OTHER_COMPETITION
    is_last_season = match.season == request.season - 1
    if is_last_season and match.competition_id == request.last_season_competition_id:
        return WindowTier.PREVIOUS_SEASON
    return None
