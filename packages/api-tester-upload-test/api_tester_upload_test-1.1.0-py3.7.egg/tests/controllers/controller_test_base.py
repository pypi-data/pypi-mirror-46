# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""

import unittest

from tester.configuration import Configuration
from tester.configuration import Environment
from tester.tester_client import TesterClient


class ControllerTestBase(unittest.TestCase):

    """All test classes inherit from this base class. It abstracts out
    common functionality and configuration variables set up."""

    @classmethod
    def setUpClass(cls):
        """Class method called once before running tests in a test class."""
        cls.request_timeout = 60
        cls.assert_precision = 0.1
        cls.config = ControllerTestBase.create_configuration()
        cls.client = TesterClient()

    @staticmethod
    def create_configuration():
        return Configuration(port = '3000', suites = 4,
                             environment = Environment.TESTING)
