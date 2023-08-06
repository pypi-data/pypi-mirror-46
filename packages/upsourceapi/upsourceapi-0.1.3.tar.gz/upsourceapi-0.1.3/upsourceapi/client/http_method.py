from enum import Enum, auto


class HttpMethod(Enum):
    GET = auto()
    PUT = auto()
    POST = auto()
    DELETE = auto()
    HEAD = auto()
    OPTIONS = auto()
    TRACE = auto()
    CONNECT = auto()
