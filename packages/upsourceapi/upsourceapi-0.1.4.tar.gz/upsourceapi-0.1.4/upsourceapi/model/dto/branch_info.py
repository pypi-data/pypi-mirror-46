from dataclasses import dataclass
from typing import Dict, Any

from upsourceapi.model.dto.branch_merge_info import BranchMergeInfo
from upsourceapi.model.dto.branch_stats import BranchStats
from upsourceapi.model.dto.can_create_branch_review import CanCreateBranchReview
from upsourceapi.model.dto.revision_info import RevisionInfo


@dataclass(frozen=True)
class BranchInfo(object):
    """BranchInfo parameters.
    :param commitsCount: Number of commits associated with the branch.
    :param filesCount: Number of files affected by the branch commits.
    :param branchingRevision: Revision where the branching took place.
    :param headRevision: Latest revision in the branch. See RevisionInfoDTO parameters.
    :param reviewInfo: See ReviewDescriptorDTO parameters.
    :param canCreateReview: A branch review can be created. See CanCreateBranchReviewDTO parameters.
    :param stats: See BranchStatsDTO parameters.
    :param mergeInfo: See BranchMergeInfoDTO parameters.
    :param isPullRequest: Whether the branch is a pull request.
    """
    commitsCount: int
    filesCount: int
    branchingRevision: str
    headRevision: RevisionInfo
    canCreateReview: CanCreateBranchReview
    stats: BranchStats
    mergeInfo: BranchMergeInfo
    isPullRequest: bool

    @classmethod
    def from_dict(cls, entry: Dict[str, Any]):
        return cls(
            commitsCount=entry['commitsCount'],
            filesCount=entry['filesCount'],
            branchingRevision=entry['branchingRevision'],
            headRevision=RevisionInfo.from_dict(entry['headRevision']),
            canCreateReview=CanCreateBranchReview.from_dict(entry['canCreateReview']),
            stats=BranchStats.from_dict(entry['stats']),
            mergeInfo=BranchMergeInfo.from_dict(entry['mergeInfo']),
            isPullRequest=entry['isPullRequest']
        )
