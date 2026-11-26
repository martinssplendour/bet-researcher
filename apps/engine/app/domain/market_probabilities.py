"""Steps 46-47 of docs/method.md: the chance a pick, or several picks on one match, wins."""

import math
from collections.abc import Sequence

from app.core.errors import DomainError
from app.domain.scoreline_model import ScorelineTable
from app.domain.selections import Selection


def selection_probability(table: ScorelineTable, selection: Selection) -> float:
    """Chance one pick wins: the sum of every scoreline where it wins."""
    return joint_probability(table, (selection,))


def joint_probability(table: ScorelineTable, selections: Sequence[Selection]) -> float:
    """Chance every pick wins together.

    Picks on the same match are linked (a home win usually comes with goals), so they are
    settled together on each scoreline rather than multiplied.
    """
    if not selections:
        raise DomainError("Give at least one selection.")
    return math.fsum(
        probability
        for home_goals, away_goals, probability in table.iter_cells()
        if all(selection.wins(home_goals, away_goals) for selection in selections)
    )
