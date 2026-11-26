"""Steps 50-51 of docs/method.md: combine picks on different matches into a ticket verdict."""

import math
from collections.abc import Sequence
from dataclasses import dataclass

from bet_researcher.core.errors import DomainError


@dataclass(frozen=True, slots=True)
class TicketEntry:
    """One match on the ticket.

    Several picks on the same match must already be combined into one chance with
    `market_probabilities.joint_probability`, because they are linked.
    """

    match_key: str
    probability: float
    offered_odds: float | None = None

    def __post_init__(self) -> None:
        if not 0.0 < self.probability <= 1.0:
            raise DomainError("A pick's chance must be above 0 and at most 1.")
        if self.offered_odds is not None and (
            not math.isfinite(self.offered_odds) or self.offered_odds <= 1.0
        ):
            raise DomainError("Decimal odds must be above 1.0.")


@dataclass(frozen=True, slots=True)
class TicketSummary:
    """The whole ticket: its chance, odds, weakest pick and what removing each pick does."""

    probability: float
    fair_odds: float
    offered_odds: float | None
    weakest: TicketEntry
    without_each: tuple[tuple[str, float], ...]


def summarize_ticket(entries: Sequence[TicketEntry]) -> TicketSummary:
    """Multiply the chances of picks on different matches and describe the result."""
    if not entries:
        raise DomainError("A ticket needs at least one pick.")
    keys = [entry.match_key for entry in entries]
    if len(set(keys)) != len(keys):
        raise DomainError("Two entries are on the same match; combine them into one chance first.")

    probability = math.prod(entry.probability for entry in entries)
    odds = [entry.offered_odds for entry in entries]
    offered = math.prod(o for o in odds if o is not None) if None not in odds else None
    without_each = (
        ()
        if len(entries) == 1
        else tuple((entry.match_key, probability / entry.probability) for entry in entries)
    )
    return TicketSummary(
        probability=probability,
        fair_odds=1.0 / probability,
        offered_odds=offered,
        weakest=min(entries, key=lambda entry: entry.probability),
        without_each=without_each,
    )
