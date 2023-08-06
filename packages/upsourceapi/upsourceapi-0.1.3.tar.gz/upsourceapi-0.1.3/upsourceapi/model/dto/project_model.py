from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectModel(object):
    """ProjectModel parameters.
    :param type: Build system type ("none" to disable code intelligence, "maven" for Maven,
                 "gradle" for Gradle, "idea" for IntelliJ IDEA).
    :param pathToModel: Path to project model.
    :param defaultJdkId: Default project JDK.
    """
    type: str = "idea"
    pathToModel: str = ""
    defaultJdkId: str = ""
