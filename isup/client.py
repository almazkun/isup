import json
import urllib.request


class Client:
    @classmethod
    def get(cls, url: str, **kwargs) -> dict:
        req = urllib.request.Request(url, **kwargs)
        with urllib.request.urlopen(req, timeout=10) as res:
            return res

    @classmethod
    def post(cls, url: str, data: dict, **kwargs) -> dict:
        req = urllib.request.Request(
            url, data=json.dumps(data).encode("utf-8"), **kwargs
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            return res


class GithubClient(Client):
    @classmethod
    def get(cls, url: str, token: str) -> dict:
        return (
            super()
            .get(
                url,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "Authorization": f"Bearer {token}",
                    "X-Github-Api-Version": "2022-11-28",
                },
            )
            .read()
            .decode("utf-8")
        )

    @classmethod
    def post(cls, url: str, token: str, data: dict) -> dict:
        return (
            super()
            .post(
                url,
                data=data,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "Authorization": f"Bearer {token}",
                    "X-Github-Api-Version": "2022-11-28",
                },
            )
            .read()
            .decode("utf-8")
        )