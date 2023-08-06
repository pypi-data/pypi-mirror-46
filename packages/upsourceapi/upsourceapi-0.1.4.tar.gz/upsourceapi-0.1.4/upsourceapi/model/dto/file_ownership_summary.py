from dataclasses import dataclass
from typing import Optional, Dict, Any

from upsourceapi.model.enum import OwnershipSummary


@dataclass(frozen=True)
class FileOwnershipSummary(object):
    filePath: str
    state: int
    userId: Optional[str] = None

    def get_state(self) -> OwnershipSummary:
        return OwnershipSummary(self.state)

    @classmethod
    def from_dict(cls, entry: Dict[str, Any]):
        return cls(
            filePath=entry['filePath'],
            state=entry['state'],
            userId=entry.get('userId')
        )
