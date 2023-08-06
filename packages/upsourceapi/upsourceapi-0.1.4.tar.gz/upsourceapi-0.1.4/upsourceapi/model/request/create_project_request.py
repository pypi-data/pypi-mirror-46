import string
from dataclasses import dataclass

from upsourceapi.model.dto import ProjectSettings


@dataclass()
class CreateProjectRequest(object):
    """CreateProjectRequestDTO
    :param newProjectId: An ID of the new Upsource project.
    :param settings: Settings of the new Upsource project.
    """
    newProjectId: str
    settings: ProjectSettings

    def __post_init__(self):
        if not self.newProjectId:
            raise ValueError('newProjectId of the new Upsource project is required parameter.')
        if self.settings is None:
            raise ValueError('Settings of the new Upsource project is required parameter.')
        self.newProjectId = self.project_id_from_name(self.newProjectId)

    @classmethod
    def project_id_from_name(cls, project_name: str) -> str:
        replace_punctuation = str.maketrans(string.punctuation, " " * len(string.punctuation))
        project_id = project_name.translate(replace_punctuation)
        project_id = project_id.replace(" ", "-")
        return project_id
