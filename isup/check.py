import asyncio
import concurrent.futures
import logging
import urllib.request
from datetime import datetime

from isup.client import Client

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"


def check_url(url: str, i:int) -> Union[int, float]:
    s = datetime.now()
    logger.debug(f" {i}--> {url}")
    e = None
    try:
        res = Client.get(url, headers={"User-Agent": USER_AGENT, "Authorization": "Token 63ddf5ebf4f09ce99d5e4467f3e38770c4d7df04"})
        code, e = res.getcode(), (datetime.now() - s).total_seconds()
    except urllib.error.HTTPError as err:
        code, e = err.getcode(), (datetime.now() - s).total_seconds()
    except Exception as err:
        code, e = str(err), (datetime.now() - s).total_seconds()
    finally:
        logger.debug(f" -->{i} {code} {e} {url}")
    return code, e


def run_in_executor(url_list: list) -> list:
    loop = asyncio.get_event_loop()
    return await asyncio.gather(*[loop.run_in_executor(executor, check_url, url, i) for i, url in enumerate(urls)])


def check_list(url_list: list, concurrency: int = 100) -> list:
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(all_urls(url_list, executor))
