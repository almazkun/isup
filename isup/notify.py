import logging
import os

from isup.client import GithubClient

logger = logging.getLogger(__name__)

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "/")
GITHUB_ORG, GITHUB_REPO = GITHUB_REPOSITORY.split("/")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
ISSUE_TITLE_PATTERN = "[DOWN-ISSUE] %s is down"
ISSUE_BODY_PATTERN = """
### Web site %s returned status code %d instead of %d.


This is an automated issue created by a [isup](https://github.com/almazkun/isup/) workflow.
List of Web sites to check is defined in [URL_LIST_TO_CHECK](https://github.com/almazkun/isup/settings/variables/actions) variables.
"""


def get_issue_list(
    owner: str = GITHUB_ORG,
    repo: str = GITHUB_REPO,
    token: str = GITHUB_TOKEN,
) -> list:
    return GithubClient.issue_list(owner, repo, token)


def create_issue(
    title: str,
    body: str,
    owner: str = GITHUB_ORG,
    repo: str = GITHUB_REPO,
    token: str = GITHUB_TOKEN,
) -> dict:
    return GithubClient.create_issue(
        owner, repo, token, data={"title": title, "body": body}
    )


def already_notified(issue_list: list, issue_title: str) -> bool:
    return any(issue_title in issue.get("title", None) for issue in issue_list)


def notify(
    url: str,
    status: int,
    expected_status: int = 200,
    issue_title_pattern: str = ISSUE_TITLE_PATTERN,
) -> None:
    logger.info(f"notify: {url} {status} {expected_status}")
    
    if status != expected_status:
        issue_title = issue_title_pattern % url
        issue_list = get_issue_list()
        if already_notified(issue_list, issue_title):
            logger.info(f"Creating issue for {url} with status {status}")
            issue_body = ISSUE_BODY_PATTERN % (url, status, expected_status)
            create_issue(issue_title, issue_body)
        else:
            logger.info(f"Already notified for {url} with status {status}")
    else:
        logger.info(f"Status {status} for {url} is OK!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python -m isup.notify <url> <status> <expected_status>")
        sys.exit(1)
    url, status, expected_status = sys.argv[1:]

    notify(url, int(status), int(expected_status))
