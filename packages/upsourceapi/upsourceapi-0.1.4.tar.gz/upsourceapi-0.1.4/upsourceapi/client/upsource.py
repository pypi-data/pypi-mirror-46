import json
from dataclasses import asdict
from enum import Enum, auto
from http.client import HTTPResponse
from typing import Any, Dict, Union
from urllib.request import Request, urlopen

from upsourceapi.client.http_method import HttpMethod
from upsourceapi.model.dto import FileInRevision, ReviewId
from upsourceapi.model.request import (
    BranchInfoRequest, CreateDiscussionRequest, CreateProjectRequest, CreateReviewRequest, FindProjectsRequest
)


class UpsourceAPIResponseType(Enum):
    TEXT = auto()
    JSON = auto()


class UpsourceAPI:
    def __init__(
            self,
            base_url: str,
            headers: Dict[str, str] = None,
            raise_error: bool = True
    ):
        """Creates UpsourceService instance.
        :param base_url:
        :param headers:
        :param raise_error: If True will raises exception when api request returns error.
        """
        if not base_url:
            raise ValueError('base_url is required parameter.')
        if headers is None:
            headers = {
                "Content-Type": "application/json;charset=utf-8"
            }
        self.base_url = base_url
        self._headers = headers
        self._raise_error = raise_error

    def add_header(self, key, val):
        self._headers[key.capitalize()] = val

    def get_all_projects(self):
        """
        :return: Returns the list of all short project infos
        """
        return self._perform_request("/getAllProjects")

    def create_project(self, create_project_dto: CreateProjectRequest, find_existed: bool = True):
        if find_existed:
            new_project_id = create_project_dto.newProjectId
            result: dict = self.find_projects(FindProjectsRequest(pattern=new_project_id))['result']
            if result.get('project'):
                projects = [project for project in result['project'] if project['projectId'] == new_project_id]
                if projects:
                    print(f'Project {create_project_dto.settings.projectName} already exists.')
                    return {}
        return self._perform_request("/createProject", create_project_dto)

    def find_projects(self, find_projects_dto: FindProjectsRequest):
        """Returns the list of projects matching a given search criteria.
        """
        return self._perform_request("/findProjects", find_projects_dto)

    def get_branch_info(self, branch_info_dto: BranchInfoRequest):
        """Returns branch info.
        """
        return self._perform_request("/getBranchInfo", branch_info_dto)

    def create_review(self, create_review_dto: CreateReviewRequest):
        """Creates a review.
        """
        return self._perform_request("/createReview", create_review_dto)

    def get_review_ownership_summary(self, review_id: ReviewId):
        """Returns the code ownership summary for a given review.
        """
        return self._perform_request("/getReviewOwnershipSummary", review_id)

    def create_discussion(self, create_discussion_dto: CreateDiscussionRequest):
        """Creates a new discussion.
        """
        return self._perform_request("/createDiscussion", create_discussion_dto)

    def get_file_content(self, file_in_revision: FileInRevision):
        """Returns the contents of the given file.
        """
        return self._perform_request("/getFileContent", file_in_revision)

    def update_vcs(self, project_name: str):
        project_id = CreateProjectRequest.project_id_from_name(project_name)
        host = self.base_url.replace("/~rpc", "")
        with urlopen(Request(f"{host}/~vcs/{project_id}")) as response:
            return self._handle_response(response, response_type=UpsourceAPIResponseType.TEXT)

    def _perform_request(self, path: str, body_dto: Any = None, method: HttpMethod = HttpMethod.POST) -> Dict[str, Any]:
        body = asdict(body_dto) if body_dto else {}
        request = self._make_request(path, body, method.name)
        with urlopen(request) as response:
            return self._handle_response(response)

    def _make_request(self, path: str, body: Dict[str, Any], method: str) -> Request:
        body_data = json.dumps(body).encode("utf-8")
        return Request(
            url=f"{self.base_url}{path}",
            data=body_data,
            headers=self._headers,
            method=method
        )

    def _handle_response(
            self,
            response: HTTPResponse,
            response_type: UpsourceAPIResponseType = UpsourceAPIResponseType.JSON
    ) -> Union[str, Dict[str, Any]]:
        decoded_response_str = response.read().decode("utf-8")
        if response_type == UpsourceAPIResponseType.TEXT:
            return decoded_response_str
        elif response_type == UpsourceAPIResponseType.JSON:
            deserialized_object = json.loads(decoded_response_str)
            if self._raise_error and deserialized_object.get('error'):
                raise Exception(deserialized_object['error']['message'])
            else:
                return deserialized_object
        else:
            raise ValueError(f"Receive unsupported UpsourceAPIResponseType {response_type}.")
