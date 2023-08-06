import json

from upsourceapi.client import UpsourceAPI
from upsourceapi.model.dto import (
    ProjectSettings, VcsSettings, VcsConfiguration, BranchInfo, ReviewId,
    Anchor, Range, FileInRevision
)
from upsourceapi.model.request import (
    CreateProjectRequest, BranchInfoRequest, FindProjectsRequest,
    CreateReviewRequest, CreateDiscussionRequest
)


def get_all_projects(service: UpsourceAPI):
    response = service.get_all_projects()
    print(response)


def get_branch_info(service: UpsourceAPI):
    get_branch_info_dto = BranchInfoRequest("release-hyperskill-org-67-77297-TEST", "master")
    response = service.get_branch_info(get_branch_info_dto)
    print(response)


def find_projects(service: UpsourceAPI):
    response = service.find_projects(FindProjectsRequest(pattern="test"))
    print(response)


def create_review(
        service: UpsourceAPI,
        project_id: str = "release-hyperskill-org-67-77297-TEST",
        branch: str = "master"
):
    get_branch_info_request_dto = BranchInfoRequest(project_id, branch)
    branch_info = BranchInfo.from_dict(
        service.get_branch_info(get_branch_info_request_dto)['result']
    )

    branch = branch if branch_info.canCreateReview.isAllowed else None
    revisions = [branch_info.headRevision.revisionId]
    create_review_request_dto = CreateReviewRequest(project_id, revisions, branch)

    response = service.create_review(create_review_request_dto)
    print(response)

    return response


def get_review_ownership_summary(
        service: UpsourceAPI,
        project_id: str = "release-hyperskill-org-67-77297-TEST",
        review_id: str = "RHOT-CR-17"
):
    review_id = ReviewId(project_id, review_id)
    response = service.get_review_ownership_summary(review_id)
    print(response)
    return response


def create_project(service: UpsourceAPI):
    project_name = "release.hyperskill.org-452-18396-title"
    project_url = "ssh://git@13.95.131.141:23/hyperskill/{}.git".format(project_name)

    with open("../identity/upsource", "r") as file:
        ssh_key = file.read()
    with open("../identity/upsource_passphrase.txt", "r") as file:
        ssh_key_passphrase = file.read()
    with open("../identity/gitlab_sync_token.txt", "r") as file:
        gitlab_sync_token = file.read()

    vcs_configuration = VcsConfiguration(
        url=project_url,
        ssh_key=ssh_key,
        ssh_key_passphrase=ssh_key_passphrase,
        sync_token=gitlab_sync_token
    )
    vcs_settings = VcsSettings([vcs_configuration])
    vcs_json_encoded_settings = json.dumps(vcs_settings.asdict())

    project_settings = ProjectSettings(
        projectName=project_name,
        vcsSettings=vcs_json_encoded_settings
    )
    create_project_dto = CreateProjectRequest(
        newProjectId=project_name,
        settings=project_settings
    )

    response = service.create_project(create_project_dto)
    print(response)


def create_discussion(
        service: UpsourceAPI,
        file_id: str = "/src/testpackage/TestClass.java",
        revision_id: str = "45b35b2b06e7ccf19612148d1b27d7cc8c154562",
        inline_in_revision: str = "45b35b2b06e7ccf19612148d1b27d7cc8c154562",
        project_id: str = "release-hyperskill-org-67-77297-TEST",
        review_id: str = "RHOT-CR-17",
        text: str = "Test"
):
    anchor = Anchor(
        range=Range(0, 0),
        fileId=file_id,
        revisionId=revision_id,
        inlineInRevision=inline_in_revision
    )
    create_discussion_request_dto = CreateDiscussionRequest(
        anchor=anchor,
        text=text,
        projectId=project_id,
        reviewId=ReviewId(project_id, reviewId=review_id)
    )

    response = service.create_discussion(create_discussion_request_dto)
    print(response)

    return response


def get_file_content(
        service: UpsourceAPI,
        project_id: str = "release-hyperskill-org-67-77297-TEST",
        revision_id: str = "45b35b2b06e7ccf19612148d1b27d7cc8c154562",
        file_name: str = "/src/testpackage/TestClass.java"
):
    response = service.get_file_content(FileInRevision(project_id, revision_id, file_name))
    print(response)
    return response


def run_review_pipeline(
        service: UpsourceAPI,
        project_id: str = "release-hyperskill-org-67-77297-TEST",
        branch: str = "master"
):
    create_review_response = create_review(service, project_id, branch)
    review_id = create_review_response['result']['reviewId']['reviewId']

    branch_info = BranchInfo.from_dict(
        service.get_branch_info(BranchInfoRequest(project_id, branch))['result']
    )
    review_ownership_summary_response = get_review_ownership_summary(service, project_id, review_id)
    files = review_ownership_summary_response['result']['files']

    create_discussion_response = create_discussion(
        service,
        file_id=files[1]['filePath'],
        revision_id=branch_info.headRevision.revisionId,
        inline_in_revision=branch_info.headRevision.revisionId,
        project_id=project_id,
        review_id=review_id
    )

    print(create_discussion_response)
    return create_discussion_response


def update_vcs(service: UpsourceAPI, project_name: str):
    update_vcs_response = service.update_vcs(project_name)
    print(update_vcs_response)
    return update_vcs_response


if __name__ == '__main__':
    import ast

    with open("/Users/jetbrains/Downloads/pycharm-submissions-hyperskill.txt", "r") as file:
        submissions = file.readlines()

    submissions = [ast.literal_eval(submission.strip()) for submission in submissions if submission]
    submissions = [submission for submission in submissions if submission and isinstance(submission, dict)]
    submissions = list(reversed(submissions))

    submission = submissions[0]
    if submission.get('edu_task'):
        try:
            edu_task = json.loads(submission['edu_task'])
            edu_task_files = [value for key, value in edu_task['task']['files'].items() if value['is_visible']]
        except json.JSONDecodeError as e:
            print(e)

    with open("../identity/upsource_auth_token.txt", "r") as file:
        upsource_auth_token = file.read()
    api = UpsourceAPI(base_url="http://13.95.131.141:8083/~rpc")
    api.add_header("Authorization", upsource_auth_token)

    # get_all_projects(service)
    # get_branch_info(service)
    # find_projects(service)
    # create_review(service)
    # get_review_ownership_summary(service)
    # create_discussion(api)
    # get_file_content(api)
    # run_review_pipeline(api)
    update_vcs(api, "localhost-test-37-43")
