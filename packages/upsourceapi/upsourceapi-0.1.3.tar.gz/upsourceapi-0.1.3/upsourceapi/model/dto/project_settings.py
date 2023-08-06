import string
from dataclasses import dataclass, field
from functools import reduce
from typing import List

from upsourceapi.model.dto.project_model import ProjectModel


@dataclass()
class ProjectSettings(object):
    """Project settings parameters.
    :param projectName: Project name.
    :param vcsSettings: VCS configuration represented as a JSON-encoded string. See VcsSettings.
    :param codeReviewIdPattern: Code review ID pattern.
    :param checkIntervalSeconds: How often to check for new commits (in seconds).
    :param projectModel: See ProjectModel parameters.
    :param runInspections: Whether to run code inspections.
    :param inspectionProfileName: Name of the inspection profile in IntelliJ IDEA.
    :param mavenSettings: The contents of maven-settings.xml.
    :param mavenProfiles: Maven profiles. Space or comma-separated list.
    :param mavenJdkName: Maven project JDK.
    :param modelConversionSystemProperties: Model conversion system properties.
    :param gradleProperties: Gradle properties.
    :param gradleInitScript: Gradle init script.
    :param defaultEncoding: Default encoding (e.g. UTF-8).
    :param defaultBranch: Default branch.
    :param ignoredFilesInReview: A newline-separated list of wildcards. Files matching the patterns
                                 specified here will be excluded from reviews.
    :param javascriptLanguageLevel: JavaScript language level (one of the following: JS_1_5, ES5,
                                    JS_1_8_5, ES6, JSX, NASHORN, FLOW).
    :param phpLanguageLevel: PHP language level (one of the following: null, 5.3.0, 5.4.0, 5.5.0,
                             5.6.0, 7, 7.1).
    :param phpExternalDependencies: List of paths to external dependencies for a PHP project.
    :param phpComposerScript: List of commands that will be run to set up PHP composer. Default
                              command is "php composer.phar install".
    :param pythonLanguageLevel: Python language level (one of the following: null, 2, 3).
    :param buildStatusReceiveToken: "login:password" credentials used to receive build status from
                                    the build server.
    :param authorCanCloseReview: In addition to CLOSE_REVIEW permission, controls whether review
                                 authors can close reviews.
    :param authorCanDeleteReview: In addition to DELETE_REVIEW permission, controls whether review
                                  authors can delete reviews.
    :param limitResolveDiscussion: In addition to EDIT_REVIEW permission, controls whether only the
                                   person that started a discussion can resolve it.
    :param skipFileContentsImport: A newline-separated list of wildcards. Files matching the patterns
                                   specified here — binaries, for example — won't be imported.
    """
    projectName: str
    vcsSettings: str
    codeReviewIdPattern: str = None
    checkIntervalSeconds: int = 300
    projectModel: ProjectModel = ProjectModel()
    runInspections: bool = True
    inspectionProfileName: str = None
    mavenSettings: str = ""
    mavenProfiles: str = ""
    mavenJdkName: str = None
    modelConversionSystemProperties: str = ""
    gradleProperties: str = ""
    gradleInitScript: str = ""
    defaultEncoding: str = ""
    defaultBranch: str = "master"
    javascriptLanguageLevel: str = "none"
    phpLanguageLevel: str = None
    phpExternalDependencies: str = None
    phpComposerScript: str = None
    pythonLanguageLevel: str = None
    buildStatusReceiveToken: str = ""
    authorCanCloseReview: bool = True
    authorCanDeleteReview: bool = True
    limitResolveDiscussion: bool = True
    skipFileContentsImport: List[str] = field(
        default_factory=lambda: ["*.bin", "*.dll", "*.exe", "*.so", "*.gitlab-ci.yml", "*Test.java"]
    )
    ignoredFilesInReview: List[str] = field(default_factory=lambda: ["test/*", "*Test.java", "*.gitlab-ci.yml"])

    def __post_init__(self):
        if not self.projectName:
            raise ValueError('Project name is required parameter.')
        if not self.vcsSettings:
            raise ValueError('VCS settings is required parameter.')
        if self.codeReviewIdPattern is None:
            replace_punctuation = str.maketrans(string.punctuation, " " * len(string.punctuation))
            without_punctuation = self.projectName.translate(replace_punctuation)
            splits = without_punctuation.split(" ")
            no_integers = [it for it in splits if not (it.isdigit()
                                                       or it[0] == '-' and it[1:].isdigit())]
            code_review_id_pattern = reduce(
                lambda result, element: result + element[0].upper(),
                no_integers,
                ""
            )
            code_review_id_pattern += "-CR-{}"
            self.codeReviewIdPattern = code_review_id_pattern
