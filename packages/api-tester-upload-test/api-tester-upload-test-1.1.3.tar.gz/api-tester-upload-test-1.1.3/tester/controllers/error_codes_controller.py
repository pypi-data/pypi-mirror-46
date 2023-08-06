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
from tester.models.complex_5 import Complex5
from tester.exceptions.exception_with_date_exception import ExceptionWithDateException
from tester.exceptions.exception_with_uuid_exception import ExceptionWithUUIDException
from tester.exceptions.exception_with_dynamic_exception import ExceptionWithDynamicException
from tester.exceptions.exception_with_precision_exception import ExceptionWithPrecisionException
from tester.exceptions.exception_with_boolean_exception import ExceptionWithBooleanException
from tester.exceptions.exception_with_long_exception import ExceptionWithLongException
from tester.exceptions.exception_with_number_exception import ExceptionWithNumberException
from tester.exceptions.exception_with_string_exception import ExceptionWithStringException
from tester.exceptions.custom_error_response_exception import CustomErrorResponseException
from tester.exceptions.exception_with_rfc_3339_date_time_exception import ExceptionWithRfc3339DateTimeException
from tester.exceptions.unix_time_stamp_exception import UnixTimeStampException
from tester.exceptions.rfc_1123_exception import Rfc1123Exception
from tester.exceptions.local_test_exception import LocalTestException
from tester.exceptions.nested_model_exception import NestedModelException

class ErrorCodesController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, client=None, call_back=None):
        super(ErrorCodesController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def date_in_exception(self):
        """Does a GET request to /error/dateInException.

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
            self.logger.info('date_in_exception called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for date_in_exception.')
            _url_path = '/error/dateInException'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for date_in_exception.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for date_in_exception.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'date_in_exception')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for date_in_exception.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for date_in_exception. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise ExceptionWithDateException('date in exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def uuid_in_exception(self):
        """Does a GET request to /error/uuidInException.

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
            self.logger.info('uuid_in_exception called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for uuid_in_exception.')
            _url_path = '/error/uuidInException'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for uuid_in_exception.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for uuid_in_exception.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'uuid_in_exception')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for uuid_in_exception.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for uuid_in_exception. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise ExceptionWithUUIDException('uuid in exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def dynamic_in_exception(self):
        """Does a GET request to /error/dynamicInException.

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
            self.logger.info('dynamic_in_exception called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for dynamic_in_exception.')
            _url_path = '/error/dynamicInException'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for dynamic_in_exception.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for dynamic_in_exception.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'dynamic_in_exception')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for dynamic_in_exception.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for dynamic_in_exception. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise ExceptionWithDynamicException('dynamic in Exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def precision_in_exception(self):
        """Does a GET request to /error/precisionInException.

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
            self.logger.info('precision_in_exception called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for precision_in_exception.')
            _url_path = '/error/precisionInException'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for precision_in_exception.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for precision_in_exception.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'precision_in_exception')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for precision_in_exception.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for precision_in_exception. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise ExceptionWithPrecisionException('precision in Exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def boolean_in_exception(self):
        """Does a GET request to /error/booleanInException.

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
            self.logger.info('boolean_in_exception called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for boolean_in_exception.')
            _url_path = '/error/booleanInException'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for boolean_in_exception.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for boolean_in_exception.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'boolean_in_exception')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for boolean_in_exception.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for boolean_in_exception. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise ExceptionWithBooleanException('Boolean in Exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def long_in_exception(self):
        """Does a GET request to /error/longInException.

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
            self.logger.info('long_in_exception called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for long_in_exception.')
            _url_path = '/error/longInException'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for long_in_exception.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for long_in_exception.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'long_in_exception')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for long_in_exception.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for long_in_exception. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise ExceptionWithLongException('long in exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def number_in_exception(self):
        """Does a GET request to /error/numberInException.

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
            self.logger.info('number_in_exception called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for number_in_exception.')
            _url_path = '/error/numberInException'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for number_in_exception.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for number_in_exception.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'number_in_exception')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for number_in_exception.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for number_in_exception. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise ExceptionWithNumberException('number in exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_exception_with_string(self):
        """Does a GET request to /error/stringInException.

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
            self.logger.info('get_exception_with_string called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_exception_with_string.')
            _url_path = '/error/stringInException'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_exception_with_string.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_exception_with_string.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_exception_with_string')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_exception_with_string.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_exception_with_string. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise ExceptionWithStringException('exception with string', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def receive_endpoint_level_exception(self):
        """Does a GET request to /error/451.

        TODO: type endpoint description here.

        Returns:
            Complex5: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('receive_endpoint_level_exception called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for receive_endpoint_level_exception.')
            _url_path = '/error/451'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for receive_endpoint_level_exception.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for receive_endpoint_level_exception.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'receive_endpoint_level_exception')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for receive_endpoint_level_exception.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for receive_endpoint_level_exception. Returning nil.')
                return None
            elif _context.response.status_code == 451:
                raise CustomErrorResponseException('caught endpoint exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, Complex5.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def receive_global_level_exception(self):
        """Does a GET request to /error/450.

        TODO: type endpoint description here.

        Returns:
            Complex5: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('receive_global_level_exception called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for receive_global_level_exception.')
            _url_path = '/error/450'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for receive_global_level_exception.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for receive_global_level_exception.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'receive_global_level_exception')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for receive_global_level_exception.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for receive_global_level_exception. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, Complex5.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def receive_exception_with_rfc_3339_datetime(self):
        """Does a GET request to /error/Rfc3339InException.

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
            self.logger.info('receive_exception_with_rfc_3339_datetime called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for receive_exception_with_rfc_3339_datetime.')
            _url_path = '/error/Rfc3339InException'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for receive_exception_with_rfc_3339_datetime.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for receive_exception_with_rfc_3339_datetime.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'receive_exception_with_rfc_3339_datetime')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for receive_exception_with_rfc_3339_datetime.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for receive_exception_with_rfc_3339_datetime. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise ExceptionWithRfc3339DateTimeException('DateTime Exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def receive_exception_with_unixtimestamp_exception(self):
        """Does a GET request to /error/unixTimeStampException.

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
            self.logger.info('receive_exception_with_unixtimestamp_exception called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for receive_exception_with_unixtimestamp_exception.')
            _url_path = '/error/unixTimeStampException'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for receive_exception_with_unixtimestamp_exception.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for receive_exception_with_unixtimestamp_exception.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'receive_exception_with_unixtimestamp_exception')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for receive_exception_with_unixtimestamp_exception.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for receive_exception_with_unixtimestamp_exception. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise UnixTimeStampException('unixtimestamp exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def receive_exception_with_rfc_1123_datetime(self):
        """Does a GET request to /error/rfc1123Exception.

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
            self.logger.info('receive_exception_with_rfc_1123_datetime called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for receive_exception_with_rfc_1123_datetime.')
            _url_path = '/error/rfc1123Exception'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for receive_exception_with_rfc_1123_datetime.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for receive_exception_with_rfc_1123_datetime.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'receive_exception_with_rfc_1123_datetime')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for receive_exception_with_rfc_1123_datetime.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for receive_exception_with_rfc_1123_datetime. Returning nil.')
                return None
            elif _context.response.status_code == 444:
                raise Rfc1123Exception('Rfc1123 Exception', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_401(self):
        """Does a GET request to /error/401.

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
            self.logger.info('get_401 called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_401.')
            _url_path = '/error/401'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_401.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_401.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_401')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_401.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_401. Returning nil.')
                return None
            elif _context.response.status_code == 401:
                raise LocalTestException('401 Local', _context)
            elif _context.response.status_code == 421:
                raise LocalTestException('Default', _context)
            elif _context.response.status_code == 431:
                raise LocalTestException('Default', _context)
            elif _context.response.status_code == 432:
                raise LocalTestException('Default', _context)
            elif _context.response.status_code == 441:
                raise LocalTestException('Default', _context)
            elif (_context.response.status_code < 200) or (_context.response.status_code > 208): 
                raise LocalTestException('Invalid response.', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_501(self):
        """Does a GET request to /error/501.

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
            self.logger.info('get_501 called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_501.')
            _url_path = '/error/501'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_501.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_501.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_501')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_501.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_501. Returning nil.')
                return None
            elif _context.response.status_code == 501:
                raise NestedModelException('error 501', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_400(self):
        """Does a GET request to /error/400.

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
            self.logger.info('get_400 called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_400.')
            _url_path = '/error/400'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_400.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_400.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_400')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_400.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_400. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_500(self):
        """Does a GET request to /error/500.

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
            self.logger.info('get_500 called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_500.')
            _url_path = '/error/500'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_500.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_500.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_500')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_500.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for get_500. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def catch_412_global_error(self):
        """Does a GET request to /error/412.

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
            self.logger.info('catch_412_global_error called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for catch_412_global_error.')
            _url_path = '/error/412'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for catch_412_global_error.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for catch_412_global_error.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'catch_412_global_error')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for catch_412_global_error.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for catch_412_global_error. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
