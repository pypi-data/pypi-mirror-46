from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class CanCreateBranchReview(object):
    """CanCreateBranchReview parameters.
    :param isAllowed: A branch review can be created.
    :param message: A message explaining the reason why a review can't be created.
    """
    isAllowed: bool
    message: Optional[str] = None

    @classmethod
    def from_dict(cls, entry: Dict[str, Any]):
        return cls(isAllowed=entry['isAllowed'], message=entry.get('message'))
