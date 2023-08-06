from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from upsourceapi.model.enum import RevisionState, RevisionReachability


@dataclass(frozen=True)
class RevisionInfo(object):
    """RevisionInfo parameters.
    :param projectId: Project ID in Upsource.
    :param revisionId: Upsource revision ID (may differ from VCS revision ID in case of a multi-root project).
    :param revisionDate: Revision date (author date in case of Git which differentiates author and committer dates).
    :param effectiveRevisionDate: Revision date that agrees with graph topology.
    :param revisionCommitMessage: Commit message of the revision.
    :param state: Revision state: none(1), found(2), imported(3).
    :param vcsRevisionId: The VCS revision ID.
    :param shortRevisionId: Short revision ID.
    :param authorId: User ID of the commit's author.
    :param reachability: Revision reachability.
    :param tags: Revision tags, if any.
    :param branchHeadLabel: Branch head labels, if any.
    :param parentRevisionIds: List of parent revisions IDs.
    """
    projectId: str
    revisionId: str
    revisionDate: int
    effectiveRevisionDate: int
    revisionCommitMessage: str
    state: int
    vcsRevisionId: str
    shortRevisionId: str
    authorId: str
    reachability: int
    tags: Optional[List[str]] = None
    branchHeadLabel: Optional[List[str]] = None
    parentRevisionIds: Optional[List[str]] = None

    def get_state(self) -> RevisionState:
        return RevisionState(self.state)

    def get_reachability(self) -> RevisionReachability:
        return RevisionReachability(self.reachability)

    @classmethod
    def from_dict(cls, entry: Dict[str, Any]):
        return cls(
            projectId=entry['projectId'],
            revisionId=entry['revisionId'],
            revisionDate=entry['revisionDate'],
            effectiveRevisionDate=entry['effectiveRevisionDate'],
            revisionCommitMessage=entry['revisionCommitMessage'],
            state=entry['state'],
            vcsRevisionId=entry['vcsRevisionId'],
            shortRevisionId=entry['shortRevisionId'],
            authorId=entry['authorId'],
            reachability=entry['reachability'],
            tags=entry['tags'] if entry.get('tags') else [],
            branchHeadLabel=entry.get('branchHeadLabel'),
            parentRevisionIds=entry.get('parentRevisionIds')
        )
