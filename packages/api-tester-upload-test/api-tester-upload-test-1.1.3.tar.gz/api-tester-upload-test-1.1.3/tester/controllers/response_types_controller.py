# -*- coding: utf-8 -*-

"""
    tester

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

import logging
from tester.api_helper import APIHelper
from tester.configuration import Configuration
from tester.controllers.base_controller import BaseController
from tester.http.auth.auth_manager import AuthManager
import dateutil.parser
from tester.models.person import Person
from tester.models.complex_1 import Complex1
from tester.models.complex_3 import Complex3
from tester.models.response_with_enum import ResponseWithEnum
from tester.models.complex_2 import Complex2
from tester.models.company import SoftwareTester
from tester.models.company import Developer
from tester.models.company import EmployeeComp
from tester.models.company import BossCompany
from tester.models.company import Company

class ResponseTypesController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, client=None, call_back=None):
        super(ResponseTypesController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def get_content_type_headers(self):
        """Does a GET request to /response/getContentType.

        TODO: type endpoint description here.

        Returns:
            void: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_content_type_headers called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_content_type_headers.')
            _url_path = '/response/getContentType'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_content_type_headers.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_content_type_headers')
            self.validate_response(_context)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_integer_array(self):
        """Does a GET request to /response/integer.

        Get an array of integers.

        Returns:
            list of int: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_integer_array called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_integer_array.')
            _url_path = '/response/integer'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_integer_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_integer_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_integer_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_integer_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_integer_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_dynamic(self):
        """Does a GET request to /response/dynamic.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_dynamic called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_dynamic.')
            _url_path = '/response/dynamic'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_dynamic.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_dynamic.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_dynamic')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_dynamic.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_dynamic. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_dynamic_array(self):
        """Does a GET request to /response/dynamic.

        TODO: type endpoint description here.

        Returns:
            mixed: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_dynamic_array called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_dynamic_array.')
            _url_path = '/response/dynamic'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_dynamic_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_dynamic_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_dynamic_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_dynamic_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_dynamic_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_3339_datetime(self):
        """Does a GET request to /response/3339datetime.

        TODO: type endpoint description here.

        Returns:
            datetime: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_3339_datetime called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_3339_datetime.')
            _url_path = '/response/3339datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_3339_datetime.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_3339_datetime')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_3339_datetime.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_3339_datetime. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.RFC3339DateTime.from_value(_context.response.raw_body).datetime

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_3339_datetime_array(self):
        """Does a GET request to /response/3339datetime.

        TODO: type endpoint description here.

        Returns:
            list of datetime: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_3339_datetime_array called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_3339_datetime_array.')
            _url_path = '/response/3339datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_3339_datetime_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_3339_datetime_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_3339_datetime_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_3339_datetime_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_3339_datetime_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return [element.datetime for element in APIHelper.json_deserialize(_context.response.raw_body, APIHelper.RFC3339DateTime.from_value)]

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_boolean(self):
        """Does a GET request to /response/boolean.

        TODO: type endpoint description here.

        Returns:
            bool: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_boolean called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_boolean.')
            _url_path = '/response/boolean'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_boolean.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_boolean')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_boolean.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_boolean. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return _context.response.raw_body == 'true'

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_boolean_array(self):
        """Does a GET request to /response/boolean.

        TODO: type endpoint description here.

        Returns:
            list of bool: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_boolean_array called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_boolean_array.')
            _url_path = '/response/boolean'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_boolean_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_boolean_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_boolean_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_boolean_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_boolean_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_headers(self):
        """Does a GET request to /response/headers.

        TODO: type endpoint description here.

        Returns:
            void: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_headers called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_headers.')
            _url_path = '/response/headers'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_headers.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_headers')
            self.validate_response(_context)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_1123_date_time(self):
        """Does a GET request to /response/1123datetime.

        TODO: type endpoint description here.

        Returns:
            datetime: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_1123_date_time called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_1123_date_time.')
            _url_path = '/response/1123datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_1123_date_time.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_1123_date_time')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_1123_date_time.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_1123_date_time. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.HttpDateTime.from_value(_context.response.raw_body).datetime

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_unix_date_time(self):
        """Does a GET request to /response/unixdatetime.

        TODO: type endpoint description here.

        Returns:
            datetime: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_unix_date_time called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_unix_date_time.')
            _url_path = '/response/unixdatetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_unix_date_time.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_unix_date_time')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_unix_date_time.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_unix_date_time. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.UnixDateTime.from_value(_context.response.raw_body).datetime

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_1123_date_time_array(self):
        """Does a GET request to /response/1123datetime.

        TODO: type endpoint description here.

        Returns:
            list of datetime: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_1123_date_time_array called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_1123_date_time_array.')
            _url_path = '/response/1123datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_1123_date_time_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_1123_date_time_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_1123_date_time_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_1123_date_time_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_1123_date_time_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return [element.datetime for element in APIHelper.json_deserialize(_context.response.raw_body, APIHelper.HttpDateTime.from_value)]

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_unix_date_time_array(self):
        """Does a GET request to /response/unixdatetime.

        TODO: type endpoint description here.

        Returns:
            list of datetime: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_unix_date_time_array called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_unix_date_time_array.')
            _url_path = '/response/unixdatetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_unix_date_time_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_unix_date_time_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_unix_date_time_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_unix_date_time_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_unix_date_time_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return [element.datetime for element in APIHelper.json_deserialize(_context.response.raw_body, APIHelper.UnixDateTime.from_value)]

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_int_enum_array(self):
        """Does a GET request to /response/enum.

        TODO: type endpoint description here.

        Returns:
            list of SuiteCode: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_int_enum_array called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_int_enum_array.')
            _url_path = '/response/enum'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True,
                'type': 'int'
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_int_enum_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_int_enum_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_int_enum_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_int_enum_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_int_enum_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_binary(self):
        """Does a GET request to /response/binary.

        gets a binary object

        Returns:
            binary: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_binary called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_binary.')
            _url_path = '/response/binary'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_binary.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, binary = True, name = 'get_binary')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_binary.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_binary. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return _context.response.raw_body

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_integer(self):
        """Does a GET request to /response/integer.

        Gets a integer response

        Returns:
            int: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_integer called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_integer.')
            _url_path = '/response/integer'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_integer.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_integer')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_integer.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_integer. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return int(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_string_enum(self):
        """Does a GET request to /response/enum.

        TODO: type endpoint description here.

        Returns:
            Days: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_string_enum called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_string_enum.')
            _url_path = '/response/enum'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'type': 'string'
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_string_enum.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_string_enum')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_string_enum.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_string_enum. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return _context.response.raw_body

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_model_array(self):
        """Does a GET request to /response/model.

        TODO: type endpoint description here.

        Returns:
            list of Person: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_model_array called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_model_array.')
            _url_path = '/response/model'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_model_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_model_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_model_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_model_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_model_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, Person.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_long(self):
        """Does a GET request to /response/long.

        TODO: type endpoint description here.

        Returns:
            long|int: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_long called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_long.')
            _url_path = '/response/long'
            _query_builder = Configuration.get_base_uri(Configuration.Server.DEFAULT)
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_long.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_long')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_long.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_long. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return int(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_model(self):
        """Does a GET request to /response/model.

        TODO: type endpoint description here.

        Returns:
            Person: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_model called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_model.')
            _url_path = '/response/model'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_model.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_model.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, Person.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_string_enum_array(self):
        """Does a GET request to /response/enum.

        TODO: type endpoint description here.

        Returns:
            list of Days: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_string_enum_array called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_string_enum_array.')
            _url_path = '/response/enum'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True,
                'type': 'string'
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_string_enum_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_string_enum_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_string_enum_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_string_enum_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_string_enum_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_int_enum(self):
        """Does a GET request to /response/enum.

        TODO: type endpoint description here.

        Returns:
            SuiteCode: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_int_enum called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_int_enum.')
            _url_path = '/response/enum'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'type': 'int'
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_int_enum.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_int_enum')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_int_enum.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_int_enum. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return int(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_precision(self):
        """Does a GET request to /response/precision.

        TODO: type endpoint description here.

        Returns:
            float: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_precision called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_precision.')
            _url_path = '/response/precision'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_precision.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_precision')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_precision.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_precision. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return float(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def return_complex_1_object(self):
        """Does a GET request to /response/complex1.

        TODO: type endpoint description here.

        Returns:
            Complex1: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('return_complex_1_object called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for return_complex_1_object.')
            _url_path = '/response/complex1'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for return_complex_1_object.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for return_complex_1_object.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'return_complex_1_object')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for return_complex_1_object.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for return_complex_1_object. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, Complex1.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def return_complex_3_object(self):
        """Does a GET request to /response/complex3.

        TODO: type endpoint description here.

        Returns:
            Complex3: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('return_complex_3_object called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for return_complex_3_object.')
            _url_path = '/response/complex3'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for return_complex_3_object.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for return_complex_3_object.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'return_complex_3_object')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for return_complex_3_object.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for return_complex_3_object. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, Complex3.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def return_response_with_enums(self):
        """Does a GET request to /response/responseWitEnum.

        TODO: type endpoint description here.

        Returns:
            ResponseWithEnum: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('return_response_with_enums called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for return_response_with_enums.')
            _url_path = '/response/responseWitEnum'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for return_response_with_enums.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for return_response_with_enums.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'return_response_with_enums')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for return_response_with_enums.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for return_response_with_enums. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ResponseWithEnum.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def return_complex_2_object(self):
        """Does a GET request to /response/complex2.

        TODO: type endpoint description here.

        Returns:
            Complex2: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('return_complex_2_object called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for return_complex_2_object.')
            _url_path = '/response/complex2'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for return_complex_2_object.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for return_complex_2_object.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'return_complex_2_object')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for return_complex_2_object.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for return_complex_2_object. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, Complex2.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def return_tester_model(self):
        """Does a GET request to /response/tester.

        TODO: type endpoint description here.

        Returns:
            SoftwareTester: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('return_tester_model called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for return_tester_model.')
            _url_path = '/response/tester'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for return_tester_model.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for return_tester_model.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'return_tester_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for return_tester_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for return_tester_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, SoftwareTester.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def return_developer_model(self):
        """Does a GET request to /response/developer.

        TODO: type endpoint description here.

        Returns:
            Developer: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('return_developer_model called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for return_developer_model.')
            _url_path = '/response/developer'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for return_developer_model.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for return_developer_model.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'return_developer_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for return_developer_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for return_developer_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, Developer.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def return_employee_model(self):
        """Does a GET request to /response/employee.

        TODO: type endpoint description here.

        Returns:
            EmployeeComp: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('return_employee_model called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for return_employee_model.')
            _url_path = '/response/employee'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for return_employee_model.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for return_employee_model.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'return_employee_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for return_employee_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for return_employee_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, EmployeeComp.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def return_boss_model(self):
        """Does a GET request to /response/boss.

        TODO: type endpoint description here.

        Returns:
            BossCompany: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('return_boss_model called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for return_boss_model.')
            _url_path = '/response/boss'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for return_boss_model.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for return_boss_model.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'return_boss_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for return_boss_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for return_boss_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, BossCompany.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def return_company_model(self):
        """Does a GET request to /response/company.

        TODO: type endpoint description here.

        Returns:
            Company: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('return_company_model called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for return_company_model.')
            _url_path = '/response/company'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for return_company_model.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for return_company_model.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'return_company_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for return_company_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for return_company_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, Company.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_date(self):
        """Does a GET request to /response/date.

        TODO: type endpoint description here.

        Returns:
            date: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_date called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_date.')
            _url_path = '/response/date'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_date.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_date')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_date.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_date. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return dateutil.parser.parse(_context.response.raw_body).date()

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_date_array(self):
        """Does a GET request to /response/date.

        TODO: type endpoint description here.

        Returns:
            list of date: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_date_array called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_date_array.')
            _url_path = '/response/date'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_date_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_date_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_date_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_date_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_date_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return [dateutil.parser.parse(element).date() for element in APIHelper.json_deserialize(_context.response.raw_body)]

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
