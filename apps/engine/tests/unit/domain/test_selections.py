from typing import Any

import pytest

from app.core.errors import DomainError
from app.domain.selections import Market, Selection

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("selection", "home", "away", "wins"),
    [
        (Selection(Market.HOME_WIN), 2, 1, True),
        (Selection(Market.HOME_WIN), 1, 1, False),
        (Selection(Market.DRAW), 1, 1, True),
        (Selection(Market.AWAY_WIN), 0, 1, True),
        (Selection(Market.HOME_OR_DRAW), 1, 1, True),
        (Selection(Market.HOME_OR_DRAW), 0, 1, False),
        (Selection(Market.AWAY_OR_DRAW), 0, 0, True),
        (Selection(Market.HOME_OR_AWAY), 1, 1, False),
        (Selection(Market.TOTAL_OVER, line=2.5), 2, 1, True),
        (Selection(Market.TOTAL_OVER, line=2.5), 1, 1, False),
        (Selection(Market.TOTAL_UNDER, line=2.5), 1, 1, True),
        (Selection(Market.BOTH_SCORE_YES), 1, 1, True),
        (Selection(Market.BOTH_SCORE_YES), 1, 0, False),
        (Selection(Market.BOTH_SCORE_NO), 2, 0, True),
        (Selection(Market.HOME_OVER, line=1.5), 2, 0, True),
        (Selection(Market.HOME_UNDER, line=1.5), 1, 3, True),
        (Selection(Market.AWAY_OVER, line=0.5), 0, 1, True),
        (Selection(Market.AWAY_UNDER, line=0.5), 3, 0, True),
        (Selection(Market.HOME_HANDICAP, line=-1.5), 2, 0, True),
        (Selection(Market.HOME_HANDICAP, line=-1.5), 1, 0, False),
        (Selection(Market.AWAY_HANDICAP, line=1.5), 1, 0, True),
        (Selection(Market.CORRECT_SCORE, score=(2, 0)), 2, 0, True),
        (Selection(Market.CORRECT_SCORE, score=(2, 0)), 2, 1, False),
    ],
)
def test_settles_each_market(selection: Selection, home: int, away: int, wins: bool) -> None:
    assert selection.wins(home, away) is wins


@pytest.mark.parametrize(
    "kwargs",
    [
        {"market": Market.TOTAL_OVER},
        {"market": Market.TOTAL_OVER, "line": 2.0},
        {"market": Market.TOTAL_UNDER, "line": -0.5},
        {"market": Market.HOME_WIN, "line": 1.5},
        {"market": Market.CORRECT_SCORE},
        {"market": Market.CORRECT_SCORE, "score": (-1, 0)},
        {"market": Market.DRAW, "score": (1, 1)},
    ],
)
def test_rejects_malformed_selections(kwargs: dict[str, Any]) -> None:
    with pytest.raises(DomainError):
        Selection(**kwargs)
