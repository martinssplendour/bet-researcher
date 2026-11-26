"""Steps 17 and 48 of docs/method.md: bookmaker odds, fair odds and value."""

import math
from collections.abc import Sequence
from enum import StrEnum

from bet_researcher.core.errors import DomainError

DEFAULT_VALUE_TOLERANCE = 0.02


class ValueVerdict(StrEnum):
    """Whether the offered odds pay more or less than the pick's chance deserves."""

    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


def implied_probabilities(decimal_odds: Sequence[float]) -> tuple[float, ...]:
    """The bookmaker's chances for a complete set of outcomes, with its margin removed."""
    inverse = _inverse_odds(decimal_odds)
    total = math.fsum(inverse)
    return tuple(value / total for value in inverse)


def bookmaker_margin(decimal_odds: Sequence[float]) -> float:
    """How far the bookmaker's chances add up beyond 100%."""
    return math.fsum(_inverse_odds(decimal_odds)) - 1.0


def fair_odds(probability: float) -> float:
    """Odds that would exactly match the chance: 1 / chance."""
    _require_probability(probability)
    return 1.0 / probability


def expected_return(probability: float, offered_odds: float) -> float:
    """Average profit per unit staked: chance x odds - 1."""
    _require_probability(probability)
    _require_odds(offered_odds)
    return probability * offered_odds - 1.0


def value_verdict(
    probability: float,
    offered_odds: float,
    tolerance: float = DEFAULT_VALUE_TOLERANCE,
) -> ValueVerdict:
    """Good if the expected return beats +tolerance, poor if below -tolerance, else fair."""
    result = expected_return(probability, offered_odds)
    if result > tolerance:
        return ValueVerdict.GOOD
    if result < -tolerance:
        return ValueVerdict.POOR
    return ValueVerdict.FAIR


def _inverse_odds(decimal_odds: Sequence[float]) -> tuple[float, ...]:
    if not decimal_odds:
        raise DomainError("Give the odds for every outcome.")
    for odds in decimal_odds:
        _require_odds(odds)
    return tuple(1.0 / odds for odds in decimal_odds)


def _require_odds(odds: float) -> None:
    if not math.isfinite(odds) or odds <= 1.0:
        raise DomainError("Decimal odds must be above 1.0.")


def _require_probability(probability: float) -> None:
    if not 0.0 < probability <= 1.0:
        raise DomainError("A chance must be above 0 and at most 1.")
