# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser

from tests.controllers.controller_test_base import ControllerTestBase
from tests.test_helper import TestHelper
from tests.http_response_catcher import HttpResponseCatcher
from tester.api_helper import APIHelper
from tester.controllers.echo_controller import EchoController


class EchoControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(EchoControllerTests, cls).setUpClass()
        cls.response_catcher = HttpResponseCatcher()
        cls.controller = EchoController(cls.config, cls.response_catcher)

    def test_check_controller_type(self):
        self.assertTrue(type(self.client.echo) is EchoController)

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


