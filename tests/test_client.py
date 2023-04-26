import urllib.error
from unittest import TestCase

from isup.client import Client, GithubClient


class TestClient(TestCase):
    test_get_url = "https://httpbin.org/get"
    test_post_url = "https://httpbin.org/post"

    def test_client_get(self):
        url = self.test_get_url
        r = Client.get(url)
        assert r.getcode() == 200
        assert r.geturl() == url
        assert r.read().decode("utf-8") == ""

    def test_client_post(self):
        url = self.test_post_url
        r = Client.post(url, {"test": "test"})
        assert r.getcode() == 200
        assert r.geturl() == url
        assert r.read().decode("utf-8") == ""


class TestGithubClient(TestCase):
    GITHUB_TOKEN = "test_token"
    test_url = "https://api.github.com/"

    def test_github_client_get(self):
        url = self.test_url
        with self.assertRaises(urllib.error.HTTPError) as e:
            GithubClient.get(url, self.GITHUB_TOKEN)
            assert e.exception.code == 401

    def test_github_client_post(self):
        url = self.test_url
        token = self.GITHUB_TOKEN
        data = {"test": "test"}
        with self.assertRaises(urllib.error.HTTPError) as e:
            GithubClient.post(url, token, data)
            assert e.exception.code == 401
