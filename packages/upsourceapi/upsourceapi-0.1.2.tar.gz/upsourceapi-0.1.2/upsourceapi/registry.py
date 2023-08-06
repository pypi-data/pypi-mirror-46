import argparse
import json

from upsourceapi.client import UpsourceAPI
from upsourceapi.model.dto import BranchInfo, ProjectSettings, ReviewId, VcsConfiguration, VcsSettings
from upsourceapi.model.request import (
    BranchInfoRequest, CreateProjectRequest, CreateReviewRequest, FindProjectsRequest
)


def _make_api_client(args: argparse.Namespace) -> UpsourceAPI:
    upsource_api = UpsourceAPI(base_url=args.base_url)
    if args.auth_token is not None:
        upsource_api.add_header("Authorization", args.auth_token)
    return upsource_api


def get_all_projects(args: argparse.Namespace):
    upsource_api = _make_api_client(args)
    return upsource_api.get_all_projects()


def create_project(args: argparse.Namespace):
    project_name = args.project_name
    project_url = args.project_url

    vcs_configuration = VcsConfiguration(
        url=project_url,
        ssh_key=args.ssh_key,
        ssh_key_passphrase=args.ssh_key_passphrase,
        sync_token=args.sync_token
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

    upsource_api = _make_api_client(args)
    return upsource_api.create_project(create_project_dto)


def find_projects(args: argparse.Namespace):
    upsource_api = _make_api_client(args)
    request = FindProjectsRequest(pattern=args.pattern, limit=int(args.limit))
    return upsource_api.find_projects(request)


def get_branch_info(args: argparse.Namespace):
    upsource_api = _make_api_client(args)
    request = BranchInfoRequest(projectId=args.project_id, branch=args.branch)
    return upsource_api.get_branch_info(request)


def create_review(args: argparse.Namespace):
    upsource_api = _make_api_client(args)

    branch_info_response = get_branch_info(args)
    branch_info = BranchInfo.from_dict(branch_info_response['result'])

    branch = args.branch if branch_info.canCreateReview.isAllowed else None
    revisions = [branch_info.headRevision.revisionId]
    create_review_request = CreateReviewRequest(args.project_id, revisions, branch)

    return upsource_api.create_review(create_review_request)


def get_review_ownership_summary(args: argparse.Namespace):
    upsource_api = _make_api_client(args)
    review_id = ReviewId(args.project_id, args.review_id)
    return upsource_api.get_review_ownership_summary(review_id)


def update_vcs(args: argparse.Namespace):
    return _make_api_client(args).update_vcs(args.project_name)
