import time
import asyncio
import concurrent.futures
import logging
import os
import urllib.request
from datetime import datetime
from typing import Union

from isup.check import check_list

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    url_list = [
        "http://localhost:8000/my/info/",
        "http://localhost:8000/my/devices/",
        "http://localhost:8000/my/reservations/",
        "http://localhost:8000/my/evaluations/",
        "http://localhost:8000/my/devices/c930da66-5bad-4468-8064-b4bfd4155308/reservations/?month=07&year=2023",
        "http://localhost:8000/my/evaluations/8e58b70e-19b4-419e-942e-2af64ff4f59d/",
    ] * 100000
    r = {}
    for c in [100, 200, 230]:
        for i in range(5):
            print(i)
            time.sleep(1)

        idx = c*2
        s = datetime.now()
        check_list(url_list[:idx], c)
        e = datetime.now()
        r[c] = [e - s, idx]
        

    for k, v in r.items():
        print(f"c{k}: per url = {round(v[0].total_seconds()/v[1], 4)} seconds")

    

"""
CMD [ "--bind", "0.0.0.0:8000", "settings.wsgi:application", "-w", "1", "--threads", "20", "--reload", "--access-logfile", "-", "--error-logfile", "-" ]
c100: per url = 0.0183 seconds
c200: per url = 0.017 seconds
c230: per url = 0.0173 seconds

CMD [ "--bind", "0.0.0.0:8000", "settings.wsgi:application", "-w", "1", "--threads", "50", "--reload", "--access-logfile", "-", "--error-logfile", "-" ]
c100: per url = 0.0183 seconds
c200: per url = 0.017 seconds
c230: per url = 0.0173 seconds

CMD [ "--bind", "0.0.0.0:8000", "settings.wsgi:application", "-w", "1", "--reload", "--access-logfile", "-", "--error-logfile", "-" ]
c100: per url = 0.0386 seconds
c200: per url = 0.0378 seconds
c230: per url = 0.0377 seconds

CMD [ "--bind", "0.0.0.0:8000", "settings.wsgi:application", "-w", "4", "--reload", "--access-logfile", "-", "--error-logfile", "-" ]
c100: per url = 0.0164 seconds
c200: per url = 0.0161 seconds
c230: per url = 0.0162 seconds

CMD [ "--bind", "0.0.0.0:8000", "settings.wsgi:application", "-w", "4",  "--threads", "20", "--reload", "--access-logfile", "-", "--error-logfile", "-" ]
c100: per url = 0.0153 seconds
c200: per url = 0.0134 seconds
c230: per url = 0.0134 seconds


CMD [ "--bind", "0.0.0.0:8000", "settings.wsgi:application", "-w", "1",  "--threads", "100", "--reload", "--access-logfile", "-", "--error-logfile", "-" ]
c100: per url = 0.0181 seconds
c200: per url = 0.0172 seconds
c230: per url = 0.0174 seconds

CMD [ "--bind", "0.0.0.0:8000", "settings.wsgi:application", "-w", "6",  "--threads", "16", "--reload", "--access-logfile", "-", "--error-logfile", "-" ]
c100: per url = 0.0141 seconds
c200: per url = 0.0124 seconds
c230: per url = 0.0122 seconds
"""
