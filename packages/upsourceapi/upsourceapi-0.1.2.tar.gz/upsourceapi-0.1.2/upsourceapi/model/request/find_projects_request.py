from dataclasses import dataclass


@dataclass(frozen=True)
class FindProjectsRequest(object):
    """FindProjectsRequestDTO
    :param pattern: Search query, e.g. part of the name.
    :param limit: Number of projects to return.
    """
    pattern: str = ''
    limit: int = 10

    def __post_init__(self):
        if self.pattern is None:
            raise ValueError('pattern is required parameter.')
        if self.limit < 0:
            raise ValueError('Illegal limit, it should not be lower than 0.')
