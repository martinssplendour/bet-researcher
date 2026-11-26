"""Bet selections the method can price, and how each is settled from a final score.

Lines are half-goals (2.5, -1.5) so no bet can end void, which keeps every selection a
clean win-or-lose question over the scoreline table.
"""

import math
from dataclasses import dataclass
from enum import StrEnum
from typing import assert_never

from app.core.errors import DomainError


class Market(StrEnum):
    """Goal-based markets covered in v1."""

    HOME_WIN = "home_win"
    DRAW = "draw"
    AWAY_WIN = "away_win"
    HOME_OR_DRAW = "home_or_draw"
    AWAY_OR_DRAW = "away_or_draw"
    HOME_OR_AWAY = "home_or_away"
    TOTAL_OVER = "total_over"
    TOTAL_UNDER = "total_under"
    BOTH_SCORE_YES = "both_score_yes"
    BOTH_SCORE_NO = "both_score_no"
    HOME_OVER = "home_over"
    HOME_UNDER = "home_under"
    AWAY_OVER = "away_over"
    AWAY_UNDER = "away_under"
    HOME_HANDICAP = "home_handicap"
    AWAY_HANDICAP = "away_handicap"
    CORRECT_SCORE = "correct_score"


GOAL_LINE_MARKETS = frozenset(
    {
        Market.TOTAL_OVER,
        Market.TOTAL_UNDER,
        Market.HOME_OVER,
        Market.HOME_UNDER,
        Market.AWAY_OVER,
        Market.AWAY_UNDER,
    }
)
HANDICAP_MARKETS = frozenset({Market.HOME_HANDICAP, Market.AWAY_HANDICAP})
LINE_MARKETS = GOAL_LINE_MARKETS | HANDICAP_MARKETS


@dataclass(frozen=True, slots=True)
class Selection:
    """One pick: a market, plus a line or a score where the market needs one."""

    market: Market
    line: float | None = None
    score: tuple[int, int] | None = None

    def __post_init__(self) -> None:
        self._validate_line()
        self._validate_score()

    def wins(self, home_goals: int, away_goals: int) -> bool:
        """Whether this pick wins with this final score."""
        line = self.line if self.line is not None else 0.0
        total = home_goals + away_goals
        match self.market:
            case Market.HOME_WIN:
                return home_goals > away_goals
            case Market.DRAW:
                return home_goals == away_goals
            case Market.AWAY_WIN:
                return away_goals > home_goals
            case Market.HOME_OR_DRAW:
                return home_goals >= away_goals
            case Market.AWAY_OR_DRAW:
                return away_goals >= home_goals
            case Market.HOME_OR_AWAY:
                return home_goals != away_goals
            case Market.TOTAL_OVER:
                return total > line
            case Market.TOTAL_UNDER:
                return total < line
            case Market.BOTH_SCORE_YES:
                return home_goals > 0 and away_goals > 0
            case Market.BOTH_SCORE_NO:
                return home_goals == 0 or away_goals == 0
            case Market.HOME_OVER:
                return home_goals > line
            case Market.HOME_UNDER:
                return home_goals < line
            case Market.AWAY_OVER:
                return away_goals > line
            case Market.AWAY_UNDER:
                return away_goals < line
            case Market.HOME_HANDICAP:
                return home_goals + line > away_goals
            case Market.AWAY_HANDICAP:
                return away_goals + line > home_goals
            case Market.CORRECT_SCORE:
                return (home_goals, away_goals) == self.score
            case _:
                assert_never(self.market)

    def _validate_line(self) -> None:
        if self.market not in LINE_MARKETS:
            if self.line is not None:
                raise DomainError(f"{self.market} does not take a line.")
            return
        if self.line is None:
            raise DomainError(f"{self.market} needs a line, such as 2.5.")
        if not math.isclose(self.line % 1, 0.5):
            raise DomainError("Lines must be half-goals, such as 2.5, so a bet can't be void.")
        if self.market in GOAL_LINE_MARKETS and self.line < 0:
            raise DomainError("Goal lines must be positive.")

    def _validate_score(self) -> None:
        if self.market is not Market.CORRECT_SCORE:
            if self.score is not None:
                raise DomainError(f"{self.market} does not take a score.")
            return
        if self.score is None or min(self.score) < 0:
            raise DomainError("A correct score needs two goal counts of zero or more.")
