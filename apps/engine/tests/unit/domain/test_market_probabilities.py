import pytest

from bet_researcher.core.errors import DomainError
from bet_researcher.domain.expected_goals import ExpectedGoals
from bet_researcher.domain.market_probabilities import joint_probability, selection_probability
from bet_researcher.domain.scoreline_model import build_scoreline_table
from bet_researcher.domain.selections import Market, Selection

pytestmark = pytest.mark.unit

TABLE = build_scoreline_table(ExpectedGoals(home=2.1, away=0.9))
HOME_WIN = Selection(Market.HOME_WIN)
OVER_2_5 = Selection(Market.TOTAL_OVER, line=2.5)


def test_home_draw_away_add_up_to_one() -> None:
    total = sum(
        selection_probability(TABLE, Selection(market))
        for market in (Market.HOME_WIN, Market.DRAW, Market.AWAY_WIN)
    )

    assert total == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("selection", "expected"),
    [
        (HOME_WIN, 0.650),
        (Selection(Market.DRAW), 0.199),
        (OVER_2_5, 0.577),
        (Selection(Market.BOTH_SCORE_YES), 0.521),
        (Selection(Market.HOME_OR_DRAW), 0.849),
    ],
)
def test_worked_example_chances(selection: Selection, expected: float) -> None:
    assert selection_probability(TABLE, selection) == pytest.approx(expected, abs=0.002)


def test_same_match_picks_are_worked_out_together() -> None:
    together = joint_probability(TABLE, [HOME_WIN, OVER_2_5])
    multiplied = selection_probability(TABLE, HOME_WIN) * selection_probability(TABLE, OVER_2_5)

    assert together == pytest.approx(0.436, abs=0.002)
    assert together > multiplied


def test_joint_of_one_pick_is_its_own_chance() -> None:
    assert joint_probability(TABLE, [HOME_WIN]) == pytest.approx(
        selection_probability(TABLE, HOME_WIN)
    )


def test_contradictory_picks_cannot_both_win() -> None:
    assert joint_probability(TABLE, [HOME_WIN, Selection(Market.AWAY_WIN)]) == 0.0


def test_joint_needs_at_least_one_pick() -> None:
    with pytest.raises(DomainError):
        joint_probability(TABLE, [])
