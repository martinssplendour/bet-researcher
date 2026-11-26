import pytest

from bet_researcher.core.errors import DomainError
from bet_researcher.domain.verdict import LabelThresholds, VerdictLabel, label_for

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("probability", "label"),
    [
        (1.0, VerdictLabel.STRONG),
        (0.70, VerdictLabel.STRONG),
        (0.6999, VerdictLabel.LIKELY),
        (0.55, VerdictLabel.LIKELY),
        (0.40, VerdictLabel.RISKY),
        (0.3999, VerdictLabel.UNLIKELY),
        (0.0, VerdictLabel.UNLIKELY),
    ],
)
def test_default_labels(probability: float, label: VerdictLabel) -> None:
    assert label_for(probability) is label


def test_custom_thresholds() -> None:
    thresholds = LabelThresholds(strong=0.8, likely=0.6, risky=0.5)

    assert label_for(0.75, thresholds) is VerdictLabel.LIKELY


@pytest.mark.parametrize(
    ("strong", "likely", "risky"),
    [(0.5, 0.6, 0.4), (0.7, 0.55, 0.0), (1.2, 0.55, 0.4)],
)
def test_thresholds_must_descend_inside_zero_to_one(
    strong: float, likely: float, risky: float
) -> None:
    with pytest.raises(DomainError):
        LabelThresholds(strong=strong, likely=likely, risky=risky)


@pytest.mark.parametrize("probability", [-0.01, 1.2])
def test_rejects_impossible_chances(probability: float) -> None:
    with pytest.raises(DomainError):
        label_for(probability)
