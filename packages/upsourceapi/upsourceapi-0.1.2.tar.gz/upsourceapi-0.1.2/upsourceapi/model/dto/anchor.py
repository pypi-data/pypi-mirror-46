from dataclasses import dataclass
from typing import Optional

from upsourceapi.model.dto.range import Range


@dataclass(frozen=True)
class Anchor(object):
    """Anchor parameters.
    :param range: Text range associated with an anchor.
    :param fileId: File associated with an anchor.
    :param revisionId: VCS revision ID.
    :param inlineInRevision: Whether a comment was left in the inline diff.
    """
    range: Optional[Range] = None
    fileId: Optional[str] = None
    revisionId: Optional[str] = None
    inlineInRevision: Optional[str] = None
