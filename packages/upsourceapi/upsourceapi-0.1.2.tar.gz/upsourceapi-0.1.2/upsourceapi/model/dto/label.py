from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Label(object):
    name: str
    id: Optional[str] = None
    colorId: Optional[str] = None
