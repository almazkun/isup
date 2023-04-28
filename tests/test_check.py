from unittest import TestCase

from isup import check
from isup import notify

class TestCheck(TestCase):
    url = "https://akun.dev"
    expected_status = 200

    def test_check_url(self):
        status, elapsed = check.check_url(self.url)

        self.assertEqual(status, self.expected_status)
        self.assertGreater(elapsed, 0)
        self.assertLessEqual(elapsed, 10)

    def test_check_url_error(self):
        url = "https://akun.dev/404"
        expected_status = 404
        status, elapsed = check.check_url(url)

        self.assertEqual(status, expected_status)
        self.assertGreater(elapsed, 0)
        self.assertLessEqual(elapsed, 10)

    def test_check_url_timeout(self):
        url = "https://doesnotexist.akun.dev"
        expected_status = 598
        status, elapsed = check.check_url(url)

        self.assertEqual(status, expected_status)
        self.assertGreater(elapsed, 0)
        self.assertLessEqual(elapsed, 10)

    def test_check_list(self):
        url_list = [self.url + f"/?i={i}" for i in range(10)]
        l = check.check_list(url_list)
        
        self.assertEqual(len(l), len(url_list))
        self.assertEqual(l[0][0], self.expected_status)
        self.assertGreater(l[0][1], 0)
        self.assertLessEqual(l[0][1], 10)


class TestNotify(TestCase):
    def test_get_issue_list(self):
        issue = notify.create_issue(
            "Test issue",
            "Test issue body",
        )
        issue_list = notify.get_issue_list()
        print (issue_list)
        print (issue)
        self.assertTrue(any(issue.get("title", None) == "Test issue" for issue in issue_list))