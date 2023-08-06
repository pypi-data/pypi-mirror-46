from dataclasses import dataclass
from typing import Dict, List

from upsourceapi.model.dto.vcs_configuration import VcsConfiguration


@dataclass(frozen=True)
class VcsSettings(object):
    mappings: List[VcsConfiguration]

    def asdict(self) -> Dict[str, List[Dict[str, str]]]:
        return {
            "mappings": [configuration.asdict() for configuration in self.mappings]
        }
