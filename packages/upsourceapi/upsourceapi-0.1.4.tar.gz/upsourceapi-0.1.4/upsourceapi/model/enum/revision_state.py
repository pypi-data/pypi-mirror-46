from enum import Enum


class RevisionState(Enum):
    NONE = 1
    FOUND = 2
    IMPORTED = 3
