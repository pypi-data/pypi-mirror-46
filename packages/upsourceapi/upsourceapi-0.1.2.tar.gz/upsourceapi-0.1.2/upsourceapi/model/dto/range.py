from dataclasses import dataclass


@dataclass(frozen=True)
class Range(object):
    """Range parameters.
    :param startOffset: Start offset of the text range.
    :param endOffset: End offset of the text range.
    """
    startOffset: int
    endOffset: int
