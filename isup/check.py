import asyncio
import concurrent.futures
import logging
import urllib.request
from datetime import datetime

from isup.client import Client

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"


def check_url(url: str) -> int:
    s = datetime.now()
    code, took = 598, 30

    try:
        code = Client.get(
            url, headers={"User-Agent": USER_AGENT}, timeout=took
        ).getcode()
    except urllib.error.HTTPError as e:
        logger.exception(e)
        code = e.code
    except Exception as e:
        logger.exception(e)

    took = (datetime.now() - s).total_seconds()
    logger.debug(f"check_url(): {url}, {code}, {took} seconds")
    return code


def run_in_executor(url_list: list) -> list:
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [loop.run_in_executor(executor, check_url, url) for url in url_list]
        loop.run_until_complete(asyncio.gather(*futures))
    loop.close()


if __name__ == "__main__":
    import sys

    url_list = [url for url in sys.argv if url.startswith("http")]
    run_in_executor(url_list)
