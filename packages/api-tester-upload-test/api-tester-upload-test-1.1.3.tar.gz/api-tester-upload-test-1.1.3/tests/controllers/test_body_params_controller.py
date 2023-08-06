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
from tester.models.number_as_optional import NumberAsOptional
from tester.models.model_with_optional_rfc_3339_date_time import ModelWithOptionalRfc3339DateTime
from tester.models.send_rfc_339_date_time import SendRfc339DateTime
from tester.models.uuid_as_optional import UuidAsOptional
from tester.models.date_as_optional import DateAsOptional
from tester.models.dynamic_as_optional import DynamicAsOptional
from tester.models.string_as_optional import StringAsOptional
from tester.models.precision_as_optional import PrecisionAsOptional
from tester.models.long_as_optional import LongAsOptional
from tester.models.unix_date_time import UnixDateTime
from tester.models.send_unix_date_time import SendUnixDateTime
from tester.models.send_rfc_1123_date_time import SendRfc1123DateTime
from tester.models.model_with_optional_rfc_1123_date_time import ModelWithOptionalRfc1123DateTime
from tester.models.boolean_as_optional import BooleanAsOptional
from tester.models.test_nstring_encoding import TestNstringEncoding
from tester.models.test_rstring_encoding import TestRstringEncoding
from tester.models.test_r_nstring_encoding import TestRNstringEncoding
from tester.models.person import Employee
from tester.models.validate import Validate
from tester.models.additional_model_parameters import AdditionalModelParameters
from tester.models.delete_body import DeleteBody
from tester.exceptions.global_test_exception import GlobalTestException


class BodyParamsControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(BodyParamsControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.body_params

    # Todo: Add description for test test_number_as_optional
    def test_number_as_optional(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"number":1}', NumberAsOptional.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_number_as_optional(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_optional_datetime_in_model_as_body
    def test_send_optional_datetime_in_model_as_body(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"dateTime":"1994-02-13T14:01:54.9571247Z"}', ModelWithOptionalRfc3339DateTime.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_optional_datetime_in_model(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_rfc_3339_date_time_in_nested_model
    def test_send_rfc_3339_date_time_in_nested_model(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"dateTime":{"dateTime":"1994-02-13T14:01:54.9571247Z"}}', SendRfc339DateTime.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_rfc_339_date_time_in_nested_models(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_uuid_as_optional
    def test_uuid_as_optional(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"uuid":"123e4567-e89b-12d3-a456-426655440000"}', UuidAsOptional.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.uuid_as_optional(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_date_as_optional
    def test_date_as_optional(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"date":"1994-02-13"}', DateAsOptional.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.date_as_optional(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_dynamic_as_optional
    def test_dynamic_as_optional(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"dynamic":{"dynamic":"test"}}', DynamicAsOptional.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.dynamic_as_optional(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_string_as_optional
    def test_string_as_optional(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"string":"test"}', StringAsOptional.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.string_as_optional(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_precision_as_optional
    def test_precision_as_optional(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"precision":1.23}', PrecisionAsOptional.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.precision_as_optional(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_long_as_optional
    def test_long_as_optional(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"long":123123}', LongAsOptional.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.long_as_optional(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_optional_unix_time_stamp_in_body
    def test_send_optional_unix_time_stamp_in_body(self):
        # Parameters for the API call
        date_time = APIHelper.UnixDateTime.from_value(1484719381).datetime

        # Perform the API call through the SDK function
        result = self.controller.send_optional_unix_date_time_in_body(date_time)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_optional_rfc_1123_in_body
    def test_send_optional_rfc_1123_in_body(self):
        # Parameters for the API call
        body = APIHelper.HttpDateTime.from_value('Sun, 06 Nov 1994 08:49:37 GMT').datetime

        # Perform the API call through the SDK function
        result = self.controller.send_optional_rfc_1123_in_body(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_test_sending_datetime_as_optional_in_plain_text_body
    def test_test_sending_datetime_as_optional_in_plain_text_body(self):
        # Parameters for the API call
        body = APIHelper.RFC3339DateTime.from_value('1994-02-13T14:01:54.9571247Z').datetime

        # Perform the API call through the SDK function
        result = self.controller.send_datetime_optional_in_endpoint(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_optional_unix_time_stamp_in_model_body
    def test_send_optional_unix_time_stamp_in_model_body(self):
        # Parameters for the API call
        date_time = APIHelper.json_deserialize('{"dateTime":1484719381}', UnixDateTime.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_optional_unix_time_stamp_in_model_body(date_time)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_optional_unix_time_stamp_in_nested_model_body
    def test_send_optional_unix_time_stamp_in_nested_model_body(self):
        # Parameters for the API call
        date_time = APIHelper.json_deserialize('{"dateTime":{"dateTime":1484719381}}', SendUnixDateTime.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_optional_unix_time_stamp_in_nested_model_body(date_time)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_test_sending_rfc_1123_date_time_in_nested_mode
    def test_test_sending_rfc_1123_date_time_in_nested_mode(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"dateTime":{"dateTime":"Sun, 06 Nov 1994 08:49:37 GMT"}}', SendRfc1123DateTime.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_rfc_1123_date_time_in_nested_model(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_optional_rfc_1123_date_time_in_model_body
    def test_send_optional_rfc_1123_date_time_in_model_body(self):
        # Parameters for the API call
        date_time = APIHelper.json_deserialize('{"dateTime":"Sun, 06 Nov 1994 08:49:37 GMT"}', ModelWithOptionalRfc1123DateTime.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_rfc_1123_date_time_in_model(date_time)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_boolean_as_optional
    def test_boolean_as_optional(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"boolean":true}', BooleanAsOptional.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.boolean_as_optional(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_with_new_line_1
    def test_send_string_with_new_line_1(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan","field":"QA"}', TestNstringEncoding.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_string_with_new_line(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_with_new_line_2
    def test_send_string_with_new_line_2(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan","field":"QA&Dev"}', TestNstringEncoding.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_string_with_new_line(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_with_new_line_3
    def test_send_string_with_new_line_3(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan&nouman","field":"QA"}', TestNstringEncoding.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_string_with_new_line(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_with_r_1
    def test_send_string_with_r_1(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan","field":"QA"}', TestRstringEncoding.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_string_with_r(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_with_r_2
    def test_send_string_with_r_2(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan","field":"QA&Dev"}', TestRstringEncoding.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_string_with_r(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_with_r_3
    def test_send_string_with_r_3(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan&nouman","field":"QA"}', TestRstringEncoding.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_string_with_r(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_in_body_with_r_n_1
    def test_send_string_in_body_with_r_n_1(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan","field":"QA"}', TestRNstringEncoding.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_string_in_body_with_r_n(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_in_body_with_r_n_2
    def test_send_string_in_body_with_r_n_2(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan","field":"QA&Dev"}', TestRNstringEncoding.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_string_in_body_with_r_n(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_in_body_with_r_n_3
    def test_send_string_in_body_with_r_n_3(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan&nouman","field":"QA"}', TestRNstringEncoding.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_string_in_body_with_r_n(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_delete_body_with_model
    def test_send_delete_body_with_model(self):
        # Parameters for the API call
        model = APIHelper.json_deserialize(
            '{"name":"Shahid Khaliq","age":5147483645,"address":"H # 531, S # 20","uid"'
            ':"123321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z'
            '","salary":20000,"department":"Software Development","joiningDay":"Saturday'
            '","workingDays":["Monday","Tuesday","Friday"],"boss":{"personType":"Boss","'
            'name":"Zeeshan Ejaz","age":5147483645,"address":"H # 531, S # 20","uid":"12'
            '3321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z","s'
            'alary":20000,"department":"Software Development","joiningDay":"Saturday","w'
            'orkingDays":["Monday","Tuesday","Friday"],"dependents":[{"name":"Future Wif'
            'e","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birthday":"'
            '1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Future Kid'
            '","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birthday":"1'
            '994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"Sun, 06 '
            'Nov 1994 08:49:37 GMT","promotedAt":1484719381},"dependents":[{"name":"Futu'
            're Wife","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birth'
            'day":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Futu'
            're Kid","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birthd'
            'ay":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"Su'
            'n, 06 Nov 1994 08:49:37 GMT"}'
            , Employee.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_delete_body_with_model(model)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_delete_body_with_model_array
    def test_send_delete_body_with_model_array(self):
        # Parameters for the API call
        models = APIHelper.json_deserialize(
            '[{"name":"Shahid Khaliq","age":5147483645,"address":"H # 531, S # 20","uid'
            '":"123321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247'
            'Z","salary":20000,"department":"Software Development","joiningDay":"Saturda'
            'y","workingDays":["Monday","Tuesday","Friday"],"boss":{"personType":"Boss",'
            '"name":"Zeeshan Ejaz","age":5147483645,"address":"H # 531, S # 20","uid":"1'
            '23321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z","'
            'salary":20000,"department":"Software Development","joiningDay":"Saturday","'
            'workingDays":["Monday","Tuesday","Friday"],"dependents":[{"name":"Future Wi'
            'fe","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birthday":'
            '"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Future Ki'
            'd","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birthday":"'
            '1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"Sun, 06'
            ' Nov 1994 08:49:37 GMT","promotedAt":1484719381},"dependents":[{"name":"Fut'
            'ure Wife","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birt'
            'hday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Fut'
            'ure Kid","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birth'
            'day":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"S'
            'un, 06 Nov 1994 08:49:37 GMT"},{"name":"Shahid Khaliq","age":5147483645,"ad'
            'dress":"H # 531, S # 20","uid":"123321","birthday":"1994-02-13","birthtime"'
            ':"1994-02-13T14:01:54.9571247Z","salary":20000,"department":"Software Devel'
            'opment","joiningDay":"Saturday","workingDays":["Monday","Tuesday","Friday"]'
            ',"boss":{"personType":"Boss","name":"Zeeshan Ejaz","age":5147483645,"addres'
            's":"H # 531, S # 20","uid":"123321","birthday":"1994-02-13","birthtime":"19'
            '94-02-13T14:01:54.9571247Z","salary":20000,"department":"Software Developme'
            'nt","joiningDay":"Saturday","workingDays":["Monday","Tuesday","Friday"],"de'
            'pendents":[{"name":"Future Wife","age":5147483649,"address":"H # 531, S # 2'
            '0","uid":"123412","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.'
            '9571247Z"},{"name":"Future Kid","age":5147483648,"address":"H # 531, S # 20'
            '","uid":"312341","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9'
            '571247Z"}],"hiredAt":"Sun, 06 Nov 1994 08:49:37 GMT","promotedAt":148471938'
            '1},"dependents":[{"name":"Future Wife","age":5147483649,"address":"H # 531,'
            ' S # 20","uid":"123412","birthday":"1994-02-13","birthtime":"1994-02-13T14:'
            '01:54.9571247Z"},{"name":"Future Kid","age":5147483648,"address":"H # 531, '
            'S # 20","uid":"312341","birthday":"1994-02-13","birthtime":"1994-02-13T14:0'
            '1:54.9571247Z"}],"hiredAt":"Sun, 06 Nov 1994 08:49:37 GMT"}]'
            , Employee.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_delete_body_with_model_array(models)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_model_array_with_body
    def test_update_model_array_with_body(self):
        # Parameters for the API call
        models = APIHelper.json_deserialize(
            '[{"name":"Shahid Khaliq","age":5147483645,"address":"H # 531, S # 20","uid'
            '":"123321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247'
            'Z","salary":20000,"department":"Software Development","joiningDay":"Saturda'
            'y","workingDays":["Monday","Tuesday","Friday"],"boss":{"personType":"Boss",'
            '"name":"Zeeshan Ejaz","age":5147483645,"address":"H # 531, S # 20","uid":"1'
            '23321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z","'
            'salary":20000,"department":"Software Development","joiningDay":"Saturday","'
            'workingDays":["Monday","Tuesday","Friday"],"dependents":[{"name":"Future Wi'
            'fe","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birthday":'
            '"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Future Ki'
            'd","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birthday":"'
            '1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"Sun, 06'
            ' Nov 1994 08:49:37 GMT","promotedAt":1484719381},"dependents":[{"name":"Fut'
            'ure Wife","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birt'
            'hday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Fut'
            'ure Kid","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birth'
            'day":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"S'
            'un, 06 Nov 1994 08:49:37 GMT"},{"name":"Shahid Khaliq","age":5147483645,"ad'
            'dress":"H # 531, S # 20","uid":"123321","birthday":"1994-02-13","birthtime"'
            ':"1994-02-13T14:01:54.9571247Z","salary":20000,"department":"Software Devel'
            'opment","joiningDay":"Saturday","workingDays":["Monday","Tuesday","Friday"]'
            ',"boss":{"personType":"Boss","name":"Zeeshan Ejaz","age":5147483645,"addres'
            's":"H # 531, S # 20","uid":"123321","birthday":"1994-02-13","birthtime":"19'
            '94-02-13T14:01:54.9571247Z","salary":20000,"department":"Software Developme'
            'nt","joiningDay":"Saturday","workingDays":["Monday","Tuesday","Friday"],"de'
            'pendents":[{"name":"Future Wife","age":5147483649,"address":"H # 531, S # 2'
            '0","uid":"123412","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.'
            '9571247Z"},{"name":"Future Kid","age":5147483648,"address":"H # 531, S # 20'
            '","uid":"312341","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9'
            '571247Z"}],"hiredAt":"Sun, 06 Nov 1994 08:49:37 GMT","promotedAt":148471938'
            '1},"dependents":[{"name":"Future Wife","age":5147483649,"address":"H # 531,'
            ' S # 20","uid":"123412","birthday":"1994-02-13","birthtime":"1994-02-13T14:'
            '01:54.9571247Z"},{"name":"Future Kid","age":5147483648,"address":"H # 531, '
            'S # 20","uid":"312341","birthday":"1994-02-13","birthtime":"1994-02-13T14:0'
            '1:54.9571247Z"}],"hiredAt":"Sun, 06 Nov 1994 08:49:37 GMT"}]'
            , Employee.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.update_model_array(models)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_string_with_body_1
    def test_update_string_with_body_1(self):
        # Parameters for the API call
        value = 'TestString'

        # Perform the API call through the SDK function
        result = self.controller.update_string_1(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_special_string_with_body_1
    def test_update_special_string_with_body_1(self):
        # Parameters for the API call
        value = '$%^!@#$%^&*'

        # Perform the API call through the SDK function
        result = self.controller.update_string_1(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_multiliner_string_with_body_1
    def test_update_multiliner_string_with_body_1(self):
        # Parameters for the API call
        value = 'TestString\nnouman'

        # Perform the API call through the SDK function
        result = self.controller.update_string_1(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_string_with_body_corner_case_1
    def test_update_string_with_body_corner_case_1(self):
        # Parameters for the API call
        value = ' '

        # Perform the API call through the SDK function
        result = self.controller.update_string_1(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_empty_string_with_body
    def test_update_empty_string_with_body(self):
        # Parameters for the API call
        value = ''

        # Perform the API call through the SDK function
        result = self.controller.update_string_1(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)

    # Todo: Add description for test test_update_string_array_with_body
    def test_update_string_array_with_body(self):
        # Parameters for the API call
        strings = APIHelper.json_deserialize('["abc","def"]')

        # Perform the API call through the SDK function
        result = self.controller.update_string_array(strings)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_enum_array
    def test_send_string_enum_array(self):
        # Parameters for the API call
        days = APIHelper.json_deserialize('["Tuesday","Saturday","Wednesday","Monday","Sunday"]')

        # Perform the API call through the SDK function
        result = self.controller.send_string_enum_array(days)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_integer_enum_array
    def test_send_integer_enum_array(self):
        # Parameters for the API call
        suites = APIHelper.json_deserialize('[1,3,4,2,3]')

        # Perform the API call through the SDK function
        result = self.controller.send_integer_enum_array(suites)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_model_with_body
    def test_update_model_with_body(self):
        # Parameters for the API call
        model = APIHelper.json_deserialize(
            '{"name":"Shahid Khaliq","age":5147483645,"address":"H # 531, S # 20","uid"'
            ':"123321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z'
            '","salary":20000,"department":"Software Development","joiningDay":"Saturday'
            '","workingDays":["Monday","Tuesday","Friday"],"boss":{"personType":"Boss","'
            'name":"Zeeshan Ejaz","age":5147483645,"address":"H # 531, S # 20","uid":"12'
            '3321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z","s'
            'alary":20000,"department":"Software Development","joiningDay":"Saturday","w'
            'orkingDays":["Monday","Tuesday","Friday"],"dependents":[{"name":"Future Wif'
            'e","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birthday":"'
            '1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Future Kid'
            '","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birthday":"1'
            '994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"Sun, 06 '
            'Nov 1994 08:49:37 GMT","promotedAt":1484719381},"dependents":[{"name":"Futu'
            're Wife","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birth'
            'day":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Futu'
            're Kid","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birthd'
            'ay":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"Su'
            'n, 06 Nov 1994 08:49:37 GMT"}'
            , Employee.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.update_model(model)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string
    def test_send_string(self):
        # Parameters for the API call
        value = 'TestString'

        # Perform the API call through the SDK function
        result = self.controller.send_string(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_multiliner_string
    def test_send_multiliner_string(self):
        # Parameters for the API call
        value = 'TestString\nnouman'

        # Perform the API call through the SDK function
        result = self.controller.send_string(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_with_special_characters
    def test_send_string_with_special_characters(self):
        # Parameters for the API call
        value = '$%^!@#$%^&*'

        # Perform the API call through the SDK function
        result = self.controller.send_string(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_with_only_space
    def test_send_string_with_only_space(self):
        # Parameters for the API call
        value = ' '

        # Perform the API call through the SDK function
        result = self.controller.send_string(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_string_with_body
    def test_update_string_with_body(self):
        # Parameters for the API call
        value = 'TestString'

        # Perform the API call through the SDK function
        result = self.controller.update_string(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_special_string_with_body
    def test_update_special_string_with_body(self):
        # Parameters for the API call
        value = '$%^!@#$%^&*'

        # Perform the API call through the SDK function
        result = self.controller.update_string(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_multiliner_string_with_body
    def test_update_multiliner_string_with_body(self):
        # Parameters for the API call
        value = 'TestString\nnouman'

        # Perform the API call through the SDK function
        result = self.controller.update_string(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_update_string_with_body_corner_case
    def test_update_string_with_body_corner_case(self):
        # Parameters for the API call
        value = ''

        # Perform the API call through the SDK function
        result = self.controller.update_string(value)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)

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
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_wrap_body_in_object
    def test_wrap_body_in_object(self):
        # Parameters for the API call
        field = 'QA'
        name = 'farhan'

        # Perform the API call through the SDK function
        result = self.controller.wrap_body_in_object(field, name)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_wrap_body_in_object_1
    def test_wrap_body_in_object_1(self):
        # Parameters for the API call
        field = ''
        name = 'farhan'

        # Perform the API call through the SDK function
        result = self.controller.wrap_body_in_object(field, name)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_wrap_body_in_object_2
    def test_wrap_body_in_object_2(self):
        # Parameters for the API call
        field = 'QA'
        name = ''

        # Perform the API call through the SDK function
        result = self.controller.wrap_body_in_object(field, name)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_wrap_body_in_object_3
    def test_wrap_body_in_object_3(self):
        # Parameters for the API call
        field = '$$'
        name = '$$'

        # Perform the API call through the SDK function
        result = self.controller.wrap_body_in_object(field, name)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_wrap_body_in_object_4
    def test_wrap_body_in_object_4(self):
        # Parameters for the API call
        field = 'QA&farhan'
        name = 'QA&farhan'

        # Perform the API call through the SDK function
        result = self.controller.wrap_body_in_object(field, name)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_validate_required_param_test
    def test_validate_required_param_test(self):
        # Parameters for the API call
        model = APIHelper.json_deserialize('{"name":"farhan","field":"QA"}', Validate.from_dictionary)
        option = '...'

        # Perform the API call through the SDK function
        result = self.controller.validate_required_parameter(model, option)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_additional_model_properties_1
    def test_additional_model_properties_1(self):
        # Parameters for the API call
        model = APIHelper.json_deserialize(
            '{"name":"farhan","field":"QA","address":"Ghori Town","Job":{"company":"API'
            'MATIC","location":"NUST"}}'
            , AdditionalModelParameters.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.additional_model_parameters_1(model)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_model
    def test_send_model(self):
        # Parameters for the API call
        model = APIHelper.json_deserialize(
            '{"name":"Shahid Khaliq","age":5147483645,"address":"H # 531, S # 20","uid"'
            ':"123321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z'
            '","salary":20000,"department":"Software Development","joiningDay":"Saturday'
            '","workingDays":["Monday","Tuesday","Friday"],"boss":{"personType":"Boss","'
            'name":"Zeeshan Ejaz","age":5147483645,"address":"H # 531, S # 20","uid":"12'
            '3321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z","s'
            'alary":20000,"department":"Software Development","joiningDay":"Saturday","w'
            'orkingDays":["Monday","Tuesday","Friday"],"dependents":[{"name":"Future Wif'
            'e","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birthday":"'
            '1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Future Kid'
            '","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birthday":"1'
            '994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"Sun, 06 '
            'Nov 1994 08:49:37 GMT","promotedAt":1484719381},"dependents":[{"name":"Futu'
            're Wife","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birth'
            'day":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Futu'
            're Kid","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birthd'
            'ay":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"Su'
            'n, 06 Nov 1994 08:49:37 GMT"}'
            , Employee.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_model(model)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_model_array
    def test_send_model_array(self):
        # Parameters for the API call
        models = APIHelper.json_deserialize(
            '[{"name":"Shahid Khaliq","age":5147483645,"address":"H # 531, S # 20","uid'
            '":"123321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247'
            'Z","salary":20000,"department":"Software Development","joiningDay":"Saturda'
            'y","workingDays":["Monday","Tuesday","Friday"],"boss":{"personType":"Boss",'
            '"name":"Zeeshan Ejaz","age":5147483645,"address":"H # 531, S # 20","uid":"1'
            '23321","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z","'
            'salary":20000,"department":"Software Development","joiningDay":"Saturday","'
            'workingDays":["Monday","Tuesday","Friday"],"dependents":[{"name":"Future Wi'
            'fe","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birthday":'
            '"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Future Ki'
            'd","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birthday":"'
            '1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"Sun, 06'
            ' Nov 1994 08:49:37 GMT","promotedAt":1484719381},"dependents":[{"name":"Fut'
            'ure Wife","age":5147483649,"address":"H # 531, S # 20","uid":"123412","birt'
            'hday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"},{"name":"Fut'
            'ure Kid","age":5147483648,"address":"H # 531, S # 20","uid":"312341","birth'
            'day":"1994-02-13","birthtime":"1994-02-13T14:01:54.9571247Z"}],"hiredAt":"S'
            'un, 06 Nov 1994 08:49:37 GMT"},{"name":"Shahid Khaliq","age":5147483645,"ad'
            'dress":"H # 531, S # 20","uid":"123321","birthday":"1994-02-13","birthtime"'
            ':"1994-02-13T14:01:54.9571247Z","salary":20000,"department":"Software Devel'
            'opment","joiningDay":"Saturday","workingDays":["Monday","Tuesday","Friday"]'
            ',"boss":{"personType":"Boss","name":"Zeeshan Ejaz","age":5147483645,"addres'
            's":"H # 531, S # 20","uid":"123321","birthday":"1994-02-13","birthtime":"19'
            '94-02-13T14:01:54.9571247Z","salary":20000,"department":"Software Developme'
            'nt","joiningDay":"Saturday","workingDays":["Monday","Tuesday","Friday"],"de'
            'pendents":[{"name":"Future Wife","age":5147483649,"address":"H # 531, S # 2'
            '0","uid":"123412","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.'
            '9571247Z"},{"name":"Future Kid","age":5147483648,"address":"H # 531, S # 20'
            '","uid":"312341","birthday":"1994-02-13","birthtime":"1994-02-13T14:01:54.9'
            '571247Z"}],"hiredAt":"Sun, 06 Nov 1994 08:49:37 GMT","promotedAt":148471938'
            '1},"dependents":[{"name":"Future Wife","age":5147483649,"address":"H # 531,'
            ' S # 20","uid":"123412","birthday":"1994-02-13","birthtime":"1994-02-13T14:'
            '01:54.9571247Z"},{"name":"Future Kid","age":5147483648,"address":"H # 531, '
            'S # 20","uid":"312341","birthday":"1994-02-13","birthtime":"1994-02-13T14:0'
            '1:54.9571247Z"}],"hiredAt":"Sun, 06 Nov 1994 08:49:37 GMT"}]'
            , Employee.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_model_array(models)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_dynamic
    def test_send_dynamic(self):
        # Parameters for the API call
        dynamic = APIHelper.json_deserialize('{"uid":"1123213","name":"Shahid"}')

        # Perform the API call through the SDK function
        result = self.controller.send_dynamic(dynamic)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_rfc_3339_date_time_array
    def test_send_rfc_3339_date_time_array(self):
        # Parameters for the API call
        datetimes = [element.datetime for element in APIHelper.json_deserialize('["1994-02-13T14:01:54.9571247Z","1994-02-13T14:01:54.9571247Z"]', APIHelper.RFC3339DateTime.from_value)]

        # Perform the API call through the SDK function
        result = self.controller.send_rfc_3339_date_time_array(datetimes)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_string_array
    def test_send_string_array(self):
        # Parameters for the API call
        sarray = APIHelper.json_deserialize('["abc","def"]')

        # Perform the API call through the SDK function
        result = self.controller.send_string_array(sarray)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_additional_model_properties
    def test_additional_model_properties(self):
        # Parameters for the API call
        model = APIHelper.json_deserialize(
            '{"name":"farhan","field":"QA","address":"Ghori Town","Job":{"company":"API'
            'MATIC","location":"NUST"}}'
            , AdditionalModelParameters.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.additional_model_parameters(model)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_unix_date_time_array
    def test_send_unix_date_time_array(self):
        # Parameters for the API call
        datetimes = [element.datetime for element in APIHelper.json_deserialize('[1484719381,1484719381]', APIHelper.UnixDateTime.from_value)]

        # Perform the API call through the SDK function
        result = self.controller.send_unix_date_time_array(datetimes)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_rfc_1123_date_time_array
    def test_send_rfc_1123_date_time_array(self):
        # Parameters for the API call
        datetimes = [element.datetime for element in APIHelper.json_deserialize('["Sun, 06 Nov 1994 08:49:37 GMT","Sun, 06 Nov 1994 08:49:37 GMT"]', APIHelper.HttpDateTime.from_value)]

        # Perform the API call through the SDK function
        result = self.controller.send_rfc_1123_date_time_array(datetimes)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_delete_plaintext_test
    def test_delete_plaintext_test(self):
        # Parameters for the API call
        text_string = 'farhan\nnouman'

        # Perform the API call through the SDK function
        result = self.controller.send_delete_plain_text(text_string)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_date_array
    def test_send_date_array(self):
        # Parameters for the API call
        dates = [dateutil.parser.parse(element).date() for element in APIHelper.json_deserialize('["1994-02-13","1994-02-13"]')]

        # Perform the API call through the SDK function
        result = self.controller.send_date_array(dates)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_rfc_3339_date_time
    def test_send_rfc_3339_date_time(self):
        # Parameters for the API call
        datetime = APIHelper.RFC3339DateTime.from_value('1994-02-13T14:01:54.9571247Z').datetime

        # Perform the API call through the SDK function
        result = self.controller.send_rfc_3339_date_time(datetime)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_rfc_1123_date_time
    def test_send_rfc_1123_date_time(self):
        # Parameters for the API call
        datetime = APIHelper.HttpDateTime.from_value('Sun, 06 Nov 1994 08:49:37 GMT').datetime

        # Perform the API call through the SDK function
        result = self.controller.send_rfc_1123_date_time(datetime)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_unix_date_time
    def test_send_unix_date_time(self):
        # Parameters for the API call
        datetime = APIHelper.UnixDateTime.from_value(1484719381).datetime

        # Perform the API call through the SDK function
        result = self.controller.send_unix_date_time(datetime)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_date
    def test_send_date(self):
        # Parameters for the API call
        date = dateutil.parser.parse('1994-02-13').date()

        # Perform the API call through the SDK function
        result = self.controller.send_date(date)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_delete_body
    def test_send_delete_body(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan","field":"QA"}', DeleteBody.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_delete_body(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_delete_body_with_multiliner_name
    def test_send_delete_body_with_multiliner_name(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan\\nnouman","field":"QA"}', DeleteBody.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_delete_body(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_delete_body_with_special_field_name
    def test_send_delete_body_with_special_field_name(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan","field":"&&&"}', DeleteBody.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_delete_body(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_delete_body_with_blank_field
    def test_send_delete_body_with_blank_field(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":"farhan","field":" "}', DeleteBody.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_delete_body(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_delete_body_with_blank_name
    def test_send_delete_body_with_blank_name(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":" ","field":"QA"}', DeleteBody.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_delete_body(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Todo: Add description for test test_send_delete_body_with_blank_name_and_field
    def test_send_delete_body_with_blank_name_and_field(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize('{"name":" ","field":" "}', DeleteBody.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.send_delete_body(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"passed":true}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


