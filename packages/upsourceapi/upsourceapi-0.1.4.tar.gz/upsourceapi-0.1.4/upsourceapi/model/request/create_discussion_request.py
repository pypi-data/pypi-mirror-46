from dataclasses import dataclass
from typing import Optional, List

from upsourceapi.model.dto import ReviewId, Label, Anchor


@dataclass(frozen=True)
class CreateDiscussionRequest(object):
    """BranchInfo parameters.
    :param anchor: See Anchor parameters.
    :param text: Text of the discussion.
    :param projectId: Project ID in Upsource.
    :param reviewId: See ReviewId parameters.
    :param markupType: Currently not in use.
    :param labels: Discussion labels. See Label parameters.
    """
    anchor: Anchor
    text: str
    projectId: str
    reviewId: Optional[ReviewId] = None
    markupType: Optional[str] = None
    labels: Optional[List[Label]] = None
