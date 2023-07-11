from isup.check import check_list
from isup.notify import notify

import argparse
import logging
import os

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    parser.add_argument("--expected-status", type=int, default=200)
    parser.add_argument("--concurrency", type=int, default=200)
    args = parser.parse_args()

    url_list = [args.url]
    concurrency = args.concurrency
    expected_status = args.expected_status

    result = check_list(url_list, concurrency)
    for url, status, elap in result:
        notify(url, status, expected_status)

if __name__ == "__main__":
    main()
