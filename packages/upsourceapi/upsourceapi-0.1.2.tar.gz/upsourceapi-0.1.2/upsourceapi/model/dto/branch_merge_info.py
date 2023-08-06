from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass(frozen=True)
class BranchMergeInfo(object):
    """BranchMergeInfo parameters.
    :param mergeFiles: The list of files that are changed in both: given branch and base branch.
    """
    mergeFiles: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, entry: Dict[str, Any]):
        return cls(entry.get('mergeFiles'))
