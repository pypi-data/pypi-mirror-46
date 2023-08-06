# -*- coding: utf-8 -*-

"""
    tester

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from tester.api_helper import APIHelper


class EchoControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(EchoControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.echo

    # Todo: Add description for test test_json_echo
    def test_json_echo(self):
        # Parameters for the API call
        input = APIHelper.json_deserialize('{"uid":"1123213","name":"Shahid"}')

        # Perform the API call through the SDK function
        result = self.controller.json_echo(input)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"body":{"uid":"1123213","name":"Shahid"}}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


