import logging
import os
import time

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
    for c in [10, 20, 30]:
        print()
        for i in range(3):
            print("\r", i, end="", flush=True)
            time.sleep(1)
        print()

        idx = c * 10

        r[c] = check_list(url_list[:idx], c)

    for r_c in r:
        print(
            f"c{r_c}: per url = {round(sum([elap for _, _, elap in r[r_c]])/len(r[r_c]), 4)} seconds"
        )


"""
CMD [ "--bind", "0.0.0.0:8000", "settings.wsgi:application", "-w", "1",  "--threads", "50"]
c100: per url = 1.6715 seconds
c200: per url = 3.4137 seconds
c230: per url = 4.0556 seconds
c100: per url = 1.9752 seconds
c200: per url = 3.6327 seconds
c230: per url = 3.7976 seconds

CMD [ "--bind", "0.0.0.0:8000", "settings.wsgi:application", "-w", "5",  "--threads", "10"]
c100: per url = 1.1605 seconds
c200: per url = 2.2858 seconds
c230: per url = 2.6144 seconds
c100: per url = 1.1819 seconds
c200: per url = 2.4359 seconds
c230: per url = 2.6717 seconds
"""
