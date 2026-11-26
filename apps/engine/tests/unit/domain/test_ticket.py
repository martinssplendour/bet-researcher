import pytest

from app.core.errors import DomainError
from app.domain.ticket import TicketEntry, summarize_ticket

pytestmark = pytest.mark.unit

TICKET = (
    TicketEntry(match_key="bayern-mainz", probability=0.65, offered_odds=1.35),
    TicketEntry(match_key="napoli-lecce", probability=0.80, offered_odds=1.25),
    TicketEntry(match_key="sociedad-getafe", probability=0.58, offered_odds=1.80),
)


def test_ticket_chance_multiplies_different_matches() -> None:
    assert summarize_ticket(TICKET).probability == pytest.approx(0.65 * 0.80 * 0.58)


def test_offered_and_fair_odds() -> None:
    summary = summarize_ticket(TICKET)

    assert summary.offered_odds == pytest.approx(1.35 * 1.25 * 1.80)
    assert summary.fair_odds == pytest.approx(1 / (0.65 * 0.80 * 0.58))


def test_weakest_pick() -> None:
    assert summarize_ticket(TICKET).weakest.match_key == "sociedad-getafe"


def test_chance_without_each_pick() -> None:
    without = dict(summarize_ticket(TICKET).without_each)

    assert without == pytest.approx(
        {"bayern-mainz": 0.464, "napoli-lecce": 0.377, "sociedad-getafe": 0.52}
    )


def test_offered_odds_unknown_if_any_pick_lacks_odds() -> None:
    entries = (*TICKET[:2], TicketEntry(match_key="x", probability=0.5))

    assert summarize_ticket(entries).offered_odds is None


def test_single_pick_has_no_removal_options() -> None:
    assert summarize_ticket(TICKET[:1]).without_each == ()


def test_rejects_an_empty_ticket() -> None:
    with pytest.raises(DomainError):
        summarize_ticket(())


def test_rejects_the_same_match_twice() -> None:
    with pytest.raises(DomainError, match="same match"):
        summarize_ticket((TICKET[0], TICKET[0]))


@pytest.mark.parametrize(
    ("probability", "odds"),
    [(0.0, None), (1.2, None), (0.5, 1.0)],
)
def test_entry_validation(probability: float, odds: float | None) -> None:
    with pytest.raises(DomainError):
        TicketEntry(match_key="m", probability=probability, offered_odds=odds)
