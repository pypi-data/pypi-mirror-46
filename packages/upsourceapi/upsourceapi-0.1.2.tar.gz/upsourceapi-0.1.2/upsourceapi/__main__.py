import argparse
import sys

from upsourceapi.registry import (
    create_project, create_review, find_projects, get_all_projects, get_branch_info, get_review_ownership_summary,
    update_vcs
)


def main():
    """
    Create all the argparse-rs and invokes the function from set_defaults().
    :return: The result of the function from set_defaults().
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Commands", dest="command")

    def add_default_args(p: argparse.ArgumentParser):
        p.add_argument("--base-url", default=None, help="Base URL of the Upsource instance.")
        p.add_argument(
            "--auth-token",
            default=None,
            help="""Upsource authorization token.
            This token will be added to the request authorization header. 
            """
        )

    # ----------------------------------------------------------------------------------------------
    get_all_projects_parser = subparsers.add_parser(
        "get-all-projects",
        help="Returns the list of all short project infos."
    )
    get_all_projects_parser.set_defaults(handler=get_all_projects)
    add_default_args(get_all_projects_parser)
    # ----------------------------------------------------------------------------------------------
    create_project_parser = subparsers.add_parser(
        "create-project",
        help="Creates a project."
    )
    create_project_parser.set_defaults(handler=create_project)
    create_project_parser.add_argument(
        "--project-name",
        default=None,
        help="Name for the new Upsource project."
    )
    create_project_parser.add_argument(
        "--project-url",
        default=None,
        help="Project URL, where repository hosts, e.g. ssh://git@example.com/example-repo.git"
    )
    create_project_parser.add_argument(
        "--ssh-key",
        default=None,
        help="Private SSH key in OpenSSH format."
    )
    create_project_parser.add_argument(
        "--ssh-key-passphrase",
        default=None,
        help="SSH key passphrase."
    )
    create_project_parser.add_argument(
        "--sync-token",
        default=None,
        help="""Anonymous access to the GitLab/GitHub API is forbidden. 
        Please provide an OAuth 2.0 token (recommended) or a personal access token, 
        which we'll use to read data from GitLab/GitHub. 
        Write requests will be performed on behalf of each individual Upsource user.
        """
    )
    add_default_args(create_project_parser)
    # ----------------------------------------------------------------------------------------------
    find_projects_parser = subparsers.add_parser(
        "find-projects",
        help="Returns the list of projects matching a given search criteria"
    )
    find_projects_parser.set_defaults(handler=find_projects)
    find_projects_parser.add_argument(
        "--pattern",
        default='',
        help="Search query, e.g. part of the name."
    )
    find_projects_parser.add_argument(
        "--limit",
        default=10,
        help="Number of projects to return."
    )
    add_default_args(find_projects_parser)
    # ----------------------------------------------------------------------------------------------
    get_branch_info_parser = subparsers.add_parser(
        "get-branch-info",
        help="Returns branch info."
    )
    get_branch_info_parser.set_defaults(handler=get_branch_info)
    get_branch_info_parser.add_argument(
        "--project-id",
        default=None,
        help="Project ID in Upsource."
    )
    get_branch_info_parser.add_argument(
        "--branch",
        default="master",
        help="Branch name."
    )
    add_default_args(get_branch_info_parser)
    # ----------------------------------------------------------------------------------------------
    create_review_parser = subparsers.add_parser(
        "create-review",
        help="Creates a review."
    )
    create_review_parser.set_defaults(handler=create_review)
    create_review_parser.add_argument(
        "--project-id",
        default=None,
        help="Project ID in Upsource."
    )
    create_review_parser.add_argument(
        "--branch",
        default="master",
        help="Branch name."
    )
    add_default_args(create_review_parser)
    # ----------------------------------------------------------------------------------------------
    get_review_ownership_summary_parser = subparsers.add_parser(
        "get-review-ownership-summary",
        help="Returns the code ownership summary for a given review."
    )
    get_review_ownership_summary_parser.set_defaults(handler=get_review_ownership_summary)
    get_review_ownership_summary_parser.add_argument(
        "--project-id",
        default=None,
        help="Project ID in Upsource."
    )
    get_review_ownership_summary_parser.add_argument(
        "--review-id",
        default=None,
        help="Review ID assigned to it when it's created."
    )
    add_default_args(get_review_ownership_summary_parser)
    # ----------------------------------------------------------------------------------------------
    update_vcs_parser = subparsers.add_parser("update-vcs", help="Updates project VCS.")
    update_vcs_parser.set_defaults(handler=update_vcs)
    update_vcs_parser.add_argument(
        "--project-name",
        default=None,
        help="Name for the new Upsource project."
    )
    add_default_args(update_vcs_parser)
    # ----------------------------------------------------------------------------------------------
    try:
        args = parser.parse_args()
        return args.handler(args)
    except AttributeError:
        return parser.print_usage()


if __name__ == "__main__":
    sys.exit(main())
