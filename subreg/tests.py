# Copyright (c) 2013 Petr Jerabek
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


import unittest
from getpass import getpass

from distlib.compat import raw_input

from subreg import ApiError
from subreg.api import Api

print("Promt your credentials to subreg.cz:")

username = raw_input("username: ")
password = getpass()


class SubRegTestCase(unittest.TestCase):
    """Tests for subreg"""

    def setUp(self):
        self.subreg = Api(username, password)

    def test_login(self):
        self.assertIsNotNone(self.subreg.ssid)

    def test_check_domain(self):
        existing_domains = ["example.com", "seznam.cz"]
        not_existing_domains = ["example-dhjasl.com", "seznam-djaksdjhaskdj.cz"]
        for domain in existing_domains:
            self.assertFalse(
                self.subreg.check_domain(domain),
                "Expected existing domain to be not available",
            )
        for domain in not_existing_domains:
            self.assertTrue(
                self.subreg.check_domain(domain),
                "Expected non-existant domain to be available",
            )

    def test_domains_list(self):
        self.assertTrue(
            isinstance(self.subreg.domains_list()["domains"], list),
            "Expected return type to be list",
        )

    def test_invalid_login(self):
        with self.assertRaises(ApiError) as cm:
            Api("invalid", "login")

        error = cm.exception
        self.assertEqual(error.major, 500)
        self.assertEqual(error.minor, 104)


if __name__ == "__main__":
    unittest.main()
