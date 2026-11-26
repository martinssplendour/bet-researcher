"""A finished match, as the analysis method sees it."""

from dataclasses import dataclass
from datetime import datetime

from bet_researcher.core.errors import DomainError


def require_timezone(moment: datetime, what: str) -> None:
    """Match times must carry a timezone: comparing naive and aware times fails."""
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise DomainError(f"{what} must include a timezone.")


@dataclass(frozen=True, slots=True)
class MatchRecord:
    """Final score of one finished match."""

    fixture_id: int
    kickoff: datetime
    season: int
    competition_id: int
    home_team_id: int
    away_team_id: int
    home_goals: int
    away_goals: int

    def __post_init__(self) -> None:
        require_timezone(self.kickoff, "Kickoff time")
        if self.home_team_id == self.away_team_id:
            raise DomainError("A match needs two different teams.")
        if self.home_goals < 0 or self.away_goals < 0:
            raise DomainError("Goals cannot be negative.")

    def involves(self, team_id: int) -> bool:
        """Whether the team played in this match."""
        return team_id in (self.home_team_id, self.away_team_id)

    def is_home(self, team_id: int) -> bool:
        """Whether the team was the home side."""
        self._require_team(team_id)
        return team_id == self.home_team_id

    def goals_for(self, team_id: int) -> int:
        """Goals the team scored."""
        return self.home_goals if self.is_home(team_id) else self.away_goals

    def goals_against(self, team_id: int) -> int:
        """Goals the team conceded."""
        return self.away_goals if self.is_home(team_id) else self.home_goals

    def _require_team(self, team_id: int) -> None:
        if not self.involves(team_id):
            raise DomainError(f"Team {team_id} did not play in fixture {self.fixture_id}.")
