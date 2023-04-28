import asyncio
import concurrent.futures
import logging
import os
import urllib.request
from datetime import datetime
from typing import Union

from isup.client import Client

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"


def check_url(url: str) -> Union[int, float]:
    s = datetime.now()
    try:
        res = Client.get(url, headers={"User-Agent": USER_AGENT})
        logger.debug(f"check_url(): {url}")
        return res.getcode(), (datetime.now() - s).total_seconds()

    except urllib.error.HTTPError as e:
        logger.exception(e)
        return e.code, (datetime.now() - s).total_seconds()
    except Exception as e:
        logger.exception(e)
        return 598, (datetime.now() - s).total_seconds()


async def all_urls(urls: list, executor: concurrent.futures.ThreadPoolExecutor) -> None:
    loop = asyncio.get_event_loop()
    return await asyncio.gather(*[loop.run_in_executor(executor, check_url, url) for url in urls])


def check_list(url_list: list) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(all_urls(url_list, executor))
