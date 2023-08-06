from dataclasses import dataclass


@dataclass(frozen=True)
class BranchInfoRequest(object):
    """BranchRequestDTO
    :param projectId: Project ID in Upsource.
    :param branch: Branch name.
    """
    projectId: str
    branch: str
