import math

import pytest

from app.core.errors import DomainError
from app.domain.expected_goals import ExpectedGoals
from app.domain.scoreline_model import build_scoreline_table, poisson_pmf

pytestmark = pytest.mark.unit

WORKED_EXAMPLE = ExpectedGoals(home=2.1, away=0.9)


def test_poisson_known_values() -> None:
    assert poisson_pmf(0, 2.1) == pytest.approx(math.exp(-2.1))
    assert poisson_pmf(2, 2.1) == pytest.approx(0.2700, abs=1e-4)


def test_poisson_with_zero_rate() -> None:
    assert poisson_pmf(0, 0.0) == 1.0
    assert poisson_pmf(3, 0.0) == 0.0


@pytest.mark.parametrize(("goals", "rate"), [(-1, 1.0), (1, -0.5)])
def test_poisson_rejects_negative_inputs(goals: int, rate: float) -> None:
    with pytest.raises(DomainError):
        poisson_pmf(goals, rate)


def test_table_probabilities_sum_to_one() -> None:
    table = build_scoreline_table(WORKED_EXAMPLE)

    assert sum(p for _, _, p in table.iter_cells()) == pytest.approx(1.0)


def test_worked_example_scorelines() -> None:
    table = build_scoreline_table(WORKED_EXAMPLE)

    assert table.probability(2, 0) == pytest.approx(0.1098, abs=1e-3)
    assert table.probability(1, 0) == pytest.approx(0.1046, abs=1e-3)
    assert table.probability(1, 1) == pytest.approx(0.0941, abs=1e-3)


def test_most_likely_scores_come_first() -> None:
    table = build_scoreline_table(WORKED_EXAMPLE)

    top = table.most_likely(3)

    assert [(home, away) for home, away, _ in top] == [(2, 0), (1, 0), (2, 1)]


def test_scores_outside_the_table_have_zero_chance() -> None:
    table = build_scoreline_table(WORKED_EXAMPLE, max_goals=10)

    assert table.max_goals == 10
    assert table.probability(11, 0) == 0.0
    assert table.probability(0, -1) == 0.0


def test_rejects_too_small_a_table() -> None:
    with pytest.raises(DomainError):
        build_scoreline_table(WORKED_EXAMPLE, max_goals=0)
