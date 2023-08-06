from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class CreateReviewRequest(object):
    """CreateReviewRequestDTO
    :param projectId: Project ID in Upsource.
    :param revisions: Revisions to attach.
    :param branch: Branch name.
    """
    projectId: str
    revisions: List[str]
    branch: Optional[str] = None
