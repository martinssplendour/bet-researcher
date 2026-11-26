"""Step 49 of docs/method.md: turn a chance into a plain verdict label."""

from dataclasses import dataclass
from enum import StrEnum

from app.core.errors import DomainError


class VerdictLabel(StrEnum):
    """Plain-language verdict shown next to each pick."""

    STRONG = "strong"
    LIKELY = "likely"
    RISKY = "risky"
    UNLIKELY = "unlikely"


@dataclass(frozen=True, slots=True)
class LabelThresholds:
    """Lowest chance that earns each label (tunable)."""

    strong: float = 0.70
    likely: float = 0.55
    risky: float = 0.40

    def __post_init__(self) -> None:
        if not 0.0 < self.risky < self.likely < self.strong <= 1.0:
            raise DomainError("Thresholds must satisfy 0 < risky < likely < strong <= 1.")


DEFAULT_LABEL_THRESHOLDS = LabelThresholds()


def label_for(
    probability: float, thresholds: LabelThresholds = DEFAULT_LABEL_THRESHOLDS
) -> VerdictLabel:
    """Label for a pick with this chance of winning."""
    if not 0.0 <= probability <= 1.0:
        raise DomainError("A chance must be between 0 and 1.")
    if probability >= thresholds.strong:
        return VerdictLabel.STRONG
    if probability >= thresholds.likely:
        return VerdictLabel.LIKELY
    if probability >= thresholds.risky:
        return VerdictLabel.RISKY
    return VerdictLabel.UNLIKELY
