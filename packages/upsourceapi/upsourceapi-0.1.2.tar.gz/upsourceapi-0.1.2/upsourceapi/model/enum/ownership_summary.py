from enum import Enum


class OwnershipSummary(Enum):
    """Describes file ownership.
    """
    OK = 1
    ONE_MAJOR = 2
    ALL_MINOR = 3
