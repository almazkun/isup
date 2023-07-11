import asyncio
import concurrent.futures
import logging
import urllib.request
from datetime import datetime
from typing import Union

from isup.client import Client

logger = logging.getLogger(__name__)


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"


def check_url(url: str, i: int) -> Union[str, int, float]:
    s = datetime.now()
    logger.debug(f" {i}--> {url}")
    elap = None
    try:
        res = Client.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Authorization": "Token 63ddf5ebf4f09ce99d5e4467f3e38770c4d7df04",
            },
        )
        code, elap = res.getcode(), (datetime.now() - s).total_seconds()
    except urllib.error.HTTPError as err:
        code, elap = err.code, (datetime.now() - s).total_seconds()
    except Exception as err:
        code, elap = str(err), (datetime.now() - s).total_seconds()
    finally:
        logger.debug(f" -->{i} {code} {elap} {url}")
    return url, code, elap


async def run_in_executor(
    url_list: list, executor: concurrent.futures.ThreadPoolExecutor
) -> list:
    loop = asyncio.get_event_loop()
    return await asyncio.gather(
        *[
            loop.run_in_executor(executor, check_url, url, i)
            for i, url in enumerate(url_list)
        ]
    )


def check_list(url_list: list, concurrency: int = 200) -> list:
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(run_in_executor(url_list, executor))


if __name__ == "__main__":
    import sys

    url_list = [url for url in sys.argv[1:] if url.startswith("http")]

    if not url_list:
        sys.stderr.write(
            "\033[91m"
            + "Usage: python -m isup.check.py <url1> <url2> ...\n"
            + "\033[0m"
        )
        sys.exit(1)

    concurrency = max(1, min(200, len(url_list)))

    sys.stderr.write(
        f"\033[92m"
        + f"Checking {len(url_list)} urls with concurrency {concurrency}...\n"
        + "\033[0m"
    )

    r = check_list(url_list, concurrency)
    for url, code, elap in r:
        sys.stdout.write(f"\033[92m{code} {elap} {url}\033[0m\n")
