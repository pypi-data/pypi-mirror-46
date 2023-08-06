from dataclasses import dataclass


@dataclass(frozen=True)
class FileInRevision(object):
    """
    :param projectId: Project ID in Upsource.
    :param revisionId: VCS revision ID.
    :param fileName: A full path to the file starting with a slash (e.g. /directory/file.txt).
    """
    projectId: str
    revisionId: str
    fileName: str
