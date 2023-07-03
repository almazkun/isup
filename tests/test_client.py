import os
import urllib.error
from unittest import TestCase

from isup.client import Client, GithubClient


class TestGithubClient(TestCase):
    def test_github_client_get(self):
        with self.assertRaises(urllib.error.HTTPError) as e:
            GithubClient.issue_list("test", "test", "test_token")

    def test_github_client_post(self):
        data = {"test": "test"}
        with self.assertRaises(urllib.error.HTTPError) as e:
            GithubClient.create_issue("test", "test", "test_token", data)
