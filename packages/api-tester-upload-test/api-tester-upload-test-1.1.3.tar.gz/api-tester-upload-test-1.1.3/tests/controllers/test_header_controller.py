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


class HeaderControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(HeaderControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.header

    # Todo: Add description for test test_send_headers
    def test_send_headers(self):
        # Parameters for the API call
        custom_header = 'TestString'
        value = 'TestString'

        # Perform the API call through the SDK function
        result = self.controller.send_headers(custom_header, value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


