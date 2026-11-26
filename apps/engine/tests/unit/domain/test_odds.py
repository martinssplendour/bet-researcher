import pytest

from app.core.errors import DomainError
from app.domain.odds import (
    ValueVerdict,
    bookmaker_margin,
    expected_return,
    fair_odds,
    implied_probabilities,
    value_verdict,
)

pytestmark = pytest.mark.unit

HOME_DRAW_AWAY = (1.35, 5.0, 8.0)


def test_implied_probabilities_remove_the_margin() -> None:
    chances = implied_probabilities(HOME_DRAW_AWAY)

    assert sum(chances) == pytest.approx(1.0)
    assert chances == pytest.approx((0.695052, 0.187663, 0.117290), abs=1e-5)


def test_bookmaker_margin() -> None:
    assert bookmaker_margin(HOME_DRAW_AWAY) == pytest.approx(0.065741, abs=1e-5)


@pytest.mark.parametrize("odds", [(), (1.0, 2.0), (0.5, 3.0)])
def test_odds_must_exist_and_exceed_one(odds: tuple[float, ...]) -> None:
    with pytest.raises(DomainError):
        implied_probabilities(odds)


def test_fair_odds() -> None:
    assert fair_odds(0.65) == pytest.approx(1.538462, abs=1e-6)
    assert fair_odds(1.0) == 1.0


@pytest.mark.parametrize("probability", [0.0, -0.1, 1.1])
def test_fair_odds_rejects_impossible_chances(probability: float) -> None:
    with pytest.raises(DomainError):
        fair_odds(probability)


def test_expected_return() -> None:
    assert expected_return(0.65, 1.35) == pytest.approx(-0.1225)


@pytest.mark.parametrize(
    ("probability", "offered", "verdict"),
    [
        (0.65, 1.35, ValueVerdict.POOR),
        (0.80, 1.25, ValueVerdict.FAIR),
        (0.58, 1.80, ValueVerdict.GOOD),
        (0.50, 2.03, ValueVerdict.FAIR),
        (0.50, 2.06, ValueVerdict.GOOD),
    ],
)
def test_value_verdicts(probability: float, offered: float, verdict: ValueVerdict) -> None:
    assert value_verdict(probability, offered) is verdict
