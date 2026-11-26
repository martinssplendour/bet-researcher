"""Application error types.

Expected failures raise one of these, so callers handle them deliberately
instead of catching broad built-in exceptions.
"""


class BetResearcherError(Exception):
    """Base class for every expected application error."""


class ConfigurationError(BetResearcherError):
    """Required configuration is missing or invalid. The app must not start."""


class DomainError(BetResearcherError, ValueError):
    """Inputs break a rule of the analysis method (docs/method.md)."""
