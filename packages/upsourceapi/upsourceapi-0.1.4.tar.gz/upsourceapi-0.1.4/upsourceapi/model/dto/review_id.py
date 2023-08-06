from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewId(object):
    """ReviewId parameters.
    :param projectId: Project ID in Upsource.
    :param reviewId: Review ID assigned to it when it's created.
    """
    projectId: str
    reviewId: str
