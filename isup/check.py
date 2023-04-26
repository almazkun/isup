import asyncio
import concurrent.futures
import logging
import os
import urllib.request
from datetime import datetime
from typing import Union

from isup.client import Client

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"


def check_url(url: str) -> Union[int, float]:
    s = datetime.now()
    try:
        res = Client.get(url, headers={"User-Agent": USER_AGENT})
        return res.getcode(), (datetime.now() - s).total_seconds()

    except urllib.error.HTTPError as e:
        logger.exception(e)
        return e.code, (datetime.now() - s).total_seconds()
    except Exception as e:
        logger.exception(e)
        return 598, (datetime.now() - s).total_seconds()


def write_to_file(
    path_to: str,
    url: str,
    status: int,
    expected_status: int,
    elapsed: float,
) -> None:
    file_name = url.split("/")[-1]
    with open(path_to + file_name, "a+") as f:
        f.write(f"{url},{status},{expected_status},{elapsed}\n")


def check_save(path_to: str, url: str, expected_status: int = 200) -> None:
    logger.debug(f"check_save(): {url} {expected_status}")
    status, elapsed = check_url(url)
    write_to_file(path_to, url, status, expected_status, elapsed)


async def all_urls(urls: list, executor: concurrent.futures.ThreadPoolExecutor) -> None:
    loop = asyncio.get_event_loop()
    func = lambda url: check_save(os.environ.get("PATH_TO_SAVE", "/tmp/"), url, 200)
    await asyncio.gather(*[loop.run_in_executor(executor, func, url) for url in urls])


def main() -> None:
    url_list = os.environ.get("URL_LIST_TO_CHECK", ",").split(",")
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(all_urls(url_list, executor))


if __name__ == "__main__":
    main()
