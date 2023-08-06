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
from tester.controllers.query_param_controller import QueryParamController


class QueryParamControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(QueryParamControllerTests, cls).setUpClass()
        cls.response_catcher = HttpResponseCatcher()
        cls.controller = QueryParamController(cls.config, cls.response_catcher)

    def test_check_controller_type(self):
        self.assertTrue(type(self.client.query_param) is QueryParamController)

    # Todo: Add description for test test_date_array
    def test_date_array(self):
        # Parameters for the API call
        dates = [dateutil.parser.parse(element).date() for element in APIHelper.json_deserialize('["1994-02-13","1994-02-13"]')]

        # Perform the API call through the SDK function
        result = self.controller.date_array(dates)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_optional_dynamic_query_param
    def test_optional_dynamic_query_param(self):
        # Parameters for the API call
        name = 'farhan'

        # dictionary for optional query parameters
        optional_query_parameters = {}
        optional_query_parameters['field'] =  'QA'

        # Perform the API call through the SDK function
        result = self.controller.optional_dynamic_query_param(name, optional_query_parameters)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_date
    def test_date(self):
        # Parameters for the API call
        date = dateutil.parser.parse('1994-02-13').date()

        # Perform the API call through the SDK function
        result = self.controller.date(date)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_unix_date_time_array
    def test_unix_date_time_array(self):
        # Parameters for the API call
        datetimes = [element.datetime for element in APIHelper.json_deserialize('[1484719381,1484719381]', APIHelper.UnixDateTime.from_value)]

        # Perform the API call through the SDK function
        result = self.controller.unix_date_time_array(datetimes)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_unix_date_time
    def test_unix_date_time(self):
        # Parameters for the API call
        datetime = APIHelper.UnixDateTime.from_value(1484719381).datetime

        # Perform the API call through the SDK function
        result = self.controller.unix_date_time(datetime)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_rfc_1123_date_time
    def test_rfc_1123_date_time(self):
        # Parameters for the API call
        datetime = APIHelper.HttpDateTime.from_value('Sun, 06 Nov 1994 08:49:37 GMT').datetime

        # Perform the API call through the SDK function
        result = self.controller.rfc_1123_date_time(datetime)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_rfc_1123_date_time_array
    def test_rfc_1123_date_time_array(self):
        # Parameters for the API call
        datetimes = [element.datetime for element in APIHelper.json_deserialize('["Sun, 06 Nov 1994 08:49:37 GMT","Sun, 06 Nov 1994 08:49:37 GMT"]', APIHelper.HttpDateTime.from_value)]

        # Perform the API call through the SDK function
        result = self.controller.rfc_1123_date_time_array(datetimes)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_rfc_3339_date_time_array
    def test_rfc_3339_date_time_array(self):
        # Parameters for the API call
        datetimes = [element.datetime for element in APIHelper.json_deserialize('["1994-02-13T14:01:54.9571247Z","1994-02-13T14:01:54.9571247Z"]', APIHelper.RFC3339DateTime.from_value)]

        # Perform the API call through the SDK function
        result = self.controller.rfc_3339_date_time_array(datetimes)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_rfc_3339_date_time
    def test_rfc_3339_date_time(self):
        # Parameters for the API call
        datetime = APIHelper.RFC3339DateTime.from_value('1994-02-13T14:01:54.9571247Z').datetime

        # Perform the API call through the SDK function
        result = self.controller.rfc_3339_date_time(datetime)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_no_params
    def test_no_params(self):

        # Perform the API call through the SDK function
        result = self.controller.no_params()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_string_param
    def test_string_param(self):
        # Parameters for the API call
        string = 'l;asd;asdwe[2304&&;\'.d??\\a\\\\\\;sd//'

        # Perform the API call through the SDK function
        result = self.controller.string_param(string)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_url_param
    def test_url_param(self):
        # Parameters for the API call
        url = 'https://www.shahidisawesome.com/and/also/a/narcissist?thisis=aparameter&another=one'

        # Perform the API call through the SDK function
        result = self.controller.url_param(url)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_number_array
    def test_number_array(self):
        # Parameters for the API call
        integers = APIHelper.json_deserialize('[1,2,3,4,5]')

        # Perform the API call through the SDK function
        result = self.controller.number_array(integers)

        # Test response code
        self.assertTrue(self.response_catcher.response.status_code in list(range(200, 209)))
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_string_array
    def test_string_array(self):
        # Parameters for the API call
        strings = APIHelper.json_deserialize('["abc","def"]')

        # Perform the API call through the SDK function
        result = self.controller.string_array(strings)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_simple_query
    def test_simple_query(self):
        # Parameters for the API call
        boolean = True
        number = 4
        string = 'TestString'

        # dictionary for optional query parameters
        optional_query_parameters = {}

        # Perform the API call through the SDK function
        result = self.controller.simple_query(boolean, number, string, optional_query_parameters)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_string_enum_array
    def test_string_enum_array(self):
        # Parameters for the API call
        days = APIHelper.json_deserialize('["Tuesday","Saturday","Wednesday","Monday","Sunday"]')

        # Perform the API call through the SDK function
        result = self.controller.string_enum_array(days)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_multiple_params
    def test_multiple_params(self):
        # Parameters for the API call
        number = 123412312
        precision = 1112.34
        string = '""test./;";12&&3asl"";"qw1&34"///..//.'
        url = 'http://www.abc.com/test?a=b&c="http://lolol.com?param=no&another=lol"'

        # Perform the API call through the SDK function
        result = self.controller.multiple_params(number, precision, string, url)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_integer_enum_array
    def test_integer_enum_array(self):
        # Parameters for the API call
        suites = APIHelper.json_deserialize('[1,3,4,2,3]')

        # Perform the API call through the SDK function
        result = self.controller.integer_enum_array(suites)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


