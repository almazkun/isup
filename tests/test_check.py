from unittest import TestCase
from isup import check

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