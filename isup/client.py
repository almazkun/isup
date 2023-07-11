import json
import urllib.request


class Client:
    @classmethod
    def get(cls, url: str, timeout: int = 10, **kwargs) -> dict:
        req = urllib.request.Request(url, **kwargs)
        return urllib.request.urlopen(req, timeout=timeout)

    @classmethod
    def post(cls, url: str, data: dict, timeout: int = 10, **kwargs) -> dict:
        req = urllib.request.Request(
            url, data=json.dumps(data).encode("utf-8"), **kwargs
        )
        return urllib.request.urlopen(req, timeout=timeout)


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

    @classmethod
    def issue_list(cls, owner: str, repo: str, token: str) -> dict:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        return cls.get(url, token)

    @classmethod
    def create_issue(cls, owner: str, repo: str, token: str, data: dict) -> dict:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        return cls.post(url, token, data)
