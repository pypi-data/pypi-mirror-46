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
from tester.models.server_response import ServerResponse

class QueryParamController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, client=None, call_back=None):
        super(QueryParamController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def multiple_params(self,
                        number,
                        precision,
                        string,
                        url):
        """Does a GET request to /query/multipleparams.

        TODO: type endpoint description here.

        Args:
            number (int): TODO: type description here. Example: 
            precision (float): TODO: type description here. Example: 
            string (string): TODO: type description here. Example: 
            url (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('multiple_params called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for multiple_params.')
            self.validate_parameters(number=number,
                                     precision=precision,
                                     string=string,
                                     url=url)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for multiple_params.')
            _url_path = '/query/multipleparams'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'number': number,
                'precision': precision,
                'string': string,
                'url': url
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for multiple_params.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for multiple_params.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'multiple_params')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for multiple_params.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for multiple_params. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def number_array(self,
                     integers):
        """Does a GET request to /query/numberarray.

        TODO: type endpoint description here.

        Args:
            integers (list of int): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('number_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for number_array.')
            self.validate_parameters(integers=integers)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for number_array.')
            _url_path = '/query/numberarray'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'integers': integers
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for number_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for number_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'number_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for number_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for number_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def string_array(self,
                     strings):
        """Does a GET request to /query/stringarray.

        TODO: type endpoint description here.

        Args:
            strings (list of string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('string_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for string_array.')
            self.validate_parameters(strings=strings)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for string_array.')
            _url_path = '/query/stringarray'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'strings': strings
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for string_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for string_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'string_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for string_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for string_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def simple_query(self,
                     boolean,
                     number,
                     string,
                     _optional_query_parameters=None):
        """Does a GET request to /query.

        TODO: type endpoint description here.

        Args:
            boolean (bool): TODO: type description here. Example: 
            number (int): TODO: type description here. Example: 
            string (string): TODO: type description here. Example: 
            _optional_form_parameters (Array, optional): Additional optional
                query parameters are supported by this endpoint

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('simple_query called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for simple_query.')
            self.validate_parameters(boolean=boolean,
                                     number=number,
                                     string=string)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for simple_query.')
            _url_path = '/query'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'boolean': boolean,
                'number': number,
                'string': string
            }
            if _query_parameters != None and _optional_query_parameters != None:
                _query_parameters.update(_optional_query_parameters)
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for simple_query.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for simple_query.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'simple_query')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for simple_query.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for simple_query. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def integer_enum_array(self,
                           suites):
        """Does a GET request to /query/integerenumarray.

        TODO: type endpoint description here.

        Args:
            suites (list of SuiteCode): TODO: type description here. Example:
                
        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('integer_enum_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for integer_enum_array.')
            self.validate_parameters(suites=suites)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for integer_enum_array.')
            _url_path = '/query/integerenumarray'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'suites': suites
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for integer_enum_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for integer_enum_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'integer_enum_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for integer_enum_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for integer_enum_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def string_enum_array(self,
                          days):
        """Does a GET request to /query/stringenumarray.

        TODO: type endpoint description here.

        Args:
            days (list of Days): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('string_enum_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for string_enum_array.')
            self.validate_parameters(days=days)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for string_enum_array.')
            _url_path = '/query/stringenumarray'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'days': days
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for string_enum_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for string_enum_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'string_enum_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for string_enum_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for string_enum_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def url_param(self,
                  url):
        """Does a GET request to /query/urlparam.

        TODO: type endpoint description here.

        Args:
            url (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('url_param called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for url_param.')
            self.validate_parameters(url=url)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for url_param.')
            _url_path = '/query/urlparam'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'url': url
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for url_param.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for url_param.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'url_param')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for url_param.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for url_param. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def no_params(self):
        """Does a GET request to /query/noparams.

        TODO: type endpoint description here.

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('no_params called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for no_params.')
            _url_path = '/query/noparams'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for no_params.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for no_params.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'no_params')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for no_params.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for no_params. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def string_param(self,
                     string):
        """Does a GET request to /query/stringparam.

        TODO: type endpoint description here.

        Args:
            string (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('string_param called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for string_param.')
            self.validate_parameters(string=string)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for string_param.')
            _url_path = '/query/stringparam'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'string': string
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for string_param.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for string_param.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'string_param')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for string_param.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for string_param. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def rfc_1123_date_time(self,
                           datetime):
        """Does a GET request to /query/rfc1123datetime.

        TODO: type endpoint description here.

        Args:
            datetime (datetime): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('rfc_1123_date_time called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for rfc_1123_date_time.')
            self.validate_parameters(datetime=datetime)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for rfc_1123_date_time.')
            _url_path = '/query/rfc1123datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'datetime': APIHelper.when_defined(APIHelper.HttpDateTime, datetime)
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for rfc_1123_date_time.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for rfc_1123_date_time.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'rfc_1123_date_time')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for rfc_1123_date_time.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for rfc_1123_date_time. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def rfc_1123_date_time_array(self,
                                 datetimes):
        """Does a GET request to /query/rfc1123datetimearray.

        TODO: type endpoint description here.

        Args:
            datetimes (list of datetime): TODO: type description here.
                Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('rfc_1123_date_time_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for rfc_1123_date_time_array.')
            self.validate_parameters(datetimes=datetimes)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for rfc_1123_date_time_array.')
            _url_path = '/query/rfc1123datetimearray'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'datetimes': [APIHelper.when_defined(APIHelper.HttpDateTime, element) for element in datetimes]
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for rfc_1123_date_time_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for rfc_1123_date_time_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'rfc_1123_date_time_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for rfc_1123_date_time_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for rfc_1123_date_time_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def rfc_3339_date_time_array(self,
                                 datetimes):
        """Does a GET request to /query/rfc3339datetimearray.

        TODO: type endpoint description here.

        Args:
            datetimes (list of datetime): TODO: type description here.
                Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('rfc_3339_date_time_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for rfc_3339_date_time_array.')
            self.validate_parameters(datetimes=datetimes)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for rfc_3339_date_time_array.')
            _url_path = '/query/rfc3339datetimearray'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'datetimes': [APIHelper.when_defined(APIHelper.RFC3339DateTime, element) for element in datetimes]
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for rfc_3339_date_time_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for rfc_3339_date_time_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'rfc_3339_date_time_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for rfc_3339_date_time_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for rfc_3339_date_time_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def rfc_3339_date_time(self,
                           datetime):
        """Does a GET request to /query/rfc3339datetime.

        TODO: type endpoint description here.

        Args:
            datetime (datetime): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('rfc_3339_date_time called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for rfc_3339_date_time.')
            self.validate_parameters(datetime=datetime)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for rfc_3339_date_time.')
            _url_path = '/query/rfc3339datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'datetime': APIHelper.when_defined(APIHelper.RFC3339DateTime, datetime)
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for rfc_3339_date_time.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for rfc_3339_date_time.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'rfc_3339_date_time')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for rfc_3339_date_time.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for rfc_3339_date_time. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def optional_dynamic_query_param(self,
                                     name,
                                     _optional_query_parameters=None):
        """Does a GET request to /query/optionalQueryParam.

        get optional dynamic query parameter

        Args:
            name (string): TODO: type description here. Example: 
            _optional_form_parameters (Array, optional): Additional optional
                query parameters are supported by this endpoint

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('optional_dynamic_query_param called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for optional_dynamic_query_param.')
            self.validate_parameters(name=name)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for optional_dynamic_query_param.')
            _url_path = '/query/optionalQueryParam'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'name': name
            }
            if _query_parameters != None and _optional_query_parameters != None:
                _query_parameters.update(_optional_query_parameters)
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for optional_dynamic_query_param.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for optional_dynamic_query_param.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'optional_dynamic_query_param')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for optional_dynamic_query_param.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for optional_dynamic_query_param. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def unix_date_time_array(self,
                             datetimes):
        """Does a GET request to /query/unixdatetimearray.

        TODO: type endpoint description here.

        Args:
            datetimes (list of datetime): TODO: type description here.
                Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('unix_date_time_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for unix_date_time_array.')
            self.validate_parameters(datetimes=datetimes)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for unix_date_time_array.')
            _url_path = '/query/unixdatetimearray'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'datetimes': [APIHelper.when_defined(APIHelper.UnixDateTime, element) for element in datetimes]
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for unix_date_time_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for unix_date_time_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'unix_date_time_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for unix_date_time_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for unix_date_time_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def unix_date_time(self,
                       datetime):
        """Does a GET request to /query/unixdatetime.

        TODO: type endpoint description here.

        Args:
            datetime (datetime): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('unix_date_time called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for unix_date_time.')
            self.validate_parameters(datetime=datetime)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for unix_date_time.')
            _url_path = '/query/unixdatetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'datetime': APIHelper.when_defined(APIHelper.UnixDateTime, datetime)
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for unix_date_time.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for unix_date_time.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'unix_date_time')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for unix_date_time.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for unix_date_time. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def date_array(self,
                   dates):
        """Does a GET request to /query/datearray.

        TODO: type endpoint description here.

        Args:
            dates (list of date): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('date_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for date_array.')
            self.validate_parameters(dates=dates)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for date_array.')
            _url_path = '/query/datearray'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'dates': dates
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for date_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for date_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'date_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for date_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for date_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def date(self,
                date):
        """Does a GET request to /query/date.

        TODO: type endpoint description here.

        Args:
            date (date): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('date called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for date.')
            self.validate_parameters(date=date)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for date.')
            _url_path = '/query/date'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'date': date
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for date.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for date.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'date')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for date.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for date. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
