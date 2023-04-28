import asyncio
import concurrent.futures
import logging
import os

from isup.client import GithubClient

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_ORG = GITHUB_REPOSITORY.split("/")[0]
GITHUB_REPO = GITHUB_REPOSITORY.split("/")[1]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
ISSUE_TITLE_PATTERN = "[HEALTH CHECK] %s is down"
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
    return GithubClient.get(f"https://api.github.com/repos/{owner}/{repo}/issues", token)


def create_issue(
    title: str,
    body: str,
    owner: str = GITHUB_ORG,
    repo: str = GITHUB_REPO,
    token: str = GITHUB_TOKEN,
) -> int:
    GithubClient.post(
        f"https://api.github.com/repos/{owner}/{repo}/issues",
        token,
        {
            "title": title,
            "body": body,
        },
    )


def should_notify(status: int, expected_status: int, issue_title: str) -> bool:
    if status != expected_status:
        issue_list = get_issue_list()
        return not already_notified(issue_list, issue_title)
    return False


def already_notified(issue_list: list, issue_title: str) -> bool:
    return any(issue_title in issue.get("title", None) for issue in issue_list)


def get_last_line(file_path: str) -> str:
    with open(file_path) as f:
        lines = f.readlines()
        if lines:
            return lines[-1]
        return None


def get_all_files_in_dir(dir_path: str) -> list:
    return [
        os.path.join(dir_path, file)
        for file in os.listdir(dir_path)
        if file != ".gitkeep"
    ]


def notify(
    url: str,
    status: int,
    expected_status: int = 200,
    issue_title_pattern: str = ISSUE_TITLE_PATTERN,
) -> None:
    logger.info(f"notify(): Notifying for {url} with status {status}")
    issue_title = issue_title_pattern % url
    if should_notify(status, expected_status, issue_title):
        logger.info(f"Creating issue for {url} with status {status}")
        issue_body = ISSUE_BODY_PATTERN % (url, status, expected_status)
        create_issue(issue_title, issue_body)


def from_line(line: str) -> tuple:
    url, status, expected_status, *_ = line.split(",")
    return (url.strip(), int(status), int(expected_status))


def notify_from_file(file: str) -> None:
    line = get_last_line(file)
    if line:
        notify(*from_line(line))


async def all_files(file_list: list, executor: concurrent.futures.Executor) -> list:
    loop = asyncio.get_event_loop()
    return await asyncio.gather(
        *[loop.run_in_executor(executor, notify_from_file, file) for file in file_list],
    )


def main():
    result_files = get_all_files_in_dir(".github/workflows/results/")
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    loop.run_until_complete(all_files(result_files, executor))


if __name__ == "__main__":
    main()
