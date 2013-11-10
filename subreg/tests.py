# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from getpass import getpass
import unittest
from subreg.api import Api

print 'Promt your credentials to subreg.cz:'

username = raw_input("username: ")
password = getpass()


class SubRegTestCase(unittest.TestCase):
    """Tests for subreg"""

    def setUp(self):
        self.subreg = Api()
        # Change to test endpoint
        self.subreg.endpoint = 'https://ote-soap.subreg.cz/cmd.php'
        self.subreg.login(username, password)

    def test_login(self):
        if not self.subreg.token:
            raise Exception

    def test_check_domain(self):
        existing_domains = ['example.com', 'seznam.cz']
        not_existing_domains = ['example-dhjasl.com', 'seznam-djaksdjhaskdj.cz']
        for domain in existing_domains:
            if self.subreg.check_domain(domain):
                raise Exception
        for domain in not_existing_domains:
            if not self.subreg.check_domain(domain):
                raise Exception


if __name__ == '__main__':
    unittest.main()
