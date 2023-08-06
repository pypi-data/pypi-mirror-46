from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class BranchStats(object):
    """BranchStats parameters.
    :param parentBranch: The branch from which the given branch originated; null if the given
                         branch is a default one or the only branch in the repository.
    :param commitsAhead: How many commits ahead of the parent branch; 0 for a default branch.
    :param commitsBehind: How many commits behind the parent branch; 0 for a default branch.
    """
    parentBranch: Optional[str] = None
    commitsAhead: int = 0
    commitsBehind: int = 0

    @classmethod
    def from_dict(cls, entry: Dict[str, Any]):
        return cls(
            parentBranch=entry.get('parentBranch'),
            commitsAhead=entry['commitsAhead'],
            commitsBehind=entry['commitsBehind']
        )
