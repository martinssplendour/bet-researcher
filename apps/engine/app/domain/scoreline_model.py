"""Step 45 of docs/method.md: the chance of every final score.

Each side's goals follow a Poisson distribution and are treated as independent. That is
a known simplification: low-scoring draws come out slightly too rare (see the method's
known limits; a Dixon-Coles correction can be added later).
"""

import math
from collections.abc import Iterator
from dataclasses import dataclass

from app.core.errors import DomainError
from app.domain.expected_goals import ExpectedGoals

DEFAULT_MAX_GOALS = 10
DEFAULT_TOP_SCORELINES = 5

Scoreline = tuple[int, int, float]


def poisson_pmf(goals: int, rate: float) -> float:
    """Chance of exactly `goals` goals when `rate` goals are expected."""
    if goals < 0 or rate < 0:
        raise DomainError("Goals and expected goals cannot be negative.")
    if rate == 0:
        return 1.0 if goals == 0 else 0.0
    return math.exp(goals * math.log(rate) - rate - math.lgamma(goals + 1))


@dataclass(frozen=True, slots=True)
class ScorelineTable:
    """`cells[home_goals][away_goals]` is the chance of that final score. Sums to 1."""

    cells: tuple[tuple[float, ...], ...]

    @property
    def max_goals(self) -> int:
        """Highest goal count per side the table covers."""
        return len(self.cells) - 1

    def probability(self, home_goals: int, away_goals: int) -> float:
        """Chance of one final score; 0 outside the table."""
        in_range = 0 <= home_goals <= self.max_goals and 0 <= away_goals <= self.max_goals
        return self.cells[home_goals][away_goals] if in_range else 0.0

    def iter_cells(self) -> Iterator[Scoreline]:
        """Every (home goals, away goals, chance) in the table."""
        for home_goals, row in enumerate(self.cells):
            for away_goals, probability in enumerate(row):
                yield home_goals, away_goals, probability

    def most_likely(self, count: int = DEFAULT_TOP_SCORELINES) -> tuple[Scoreline, ...]:
        """The `count` likeliest final scores, likeliest first."""
        return tuple(sorted(self.iter_cells(), key=lambda cell: cell[2], reverse=True)[:count])


def build_scoreline_table(
    expected: ExpectedGoals, max_goals: int = DEFAULT_MAX_GOALS
) -> ScorelineTable:
    """Build the table, rescaled so the cut-off tail beyond `max_goals` loses no probability."""
    if max_goals < 1:
        raise DomainError("The scoreline table must cover at least one goal per side.")
    home = [poisson_pmf(goals, expected.home) for goals in range(max_goals + 1)]
    away = [poisson_pmf(goals, expected.away) for goals in range(max_goals + 1)]
    total = math.fsum(home) * math.fsum(away)
    return ScorelineTable(
        cells=tuple(tuple(h * a / total for a in away) for h in home),
    )
