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


class TemplateParamsControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(TemplateParamsControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.template_params

    # Todo: Add description for test test_send_string_array
    def test_send_string_array(self):
        # Parameters for the API call
        strings = APIHelper.json_deserialize('["abc","def"]')

        # Perform the API call through the SDK function
        result = self.controller.send_string_array(strings)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"path":"/abc/def"}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_integer_array
    def test_send_integer_array(self):
        # Parameters for the API call
        integers = APIHelper.json_deserialize('[1,2,3,4,5]')

        # Perform the API call through the SDK function
        result = self.controller.send_integer_array(integers)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"path":"/1/2/3/4/5"}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


