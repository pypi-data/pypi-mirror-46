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

class QueryParamsController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, client=None, call_back=None):
        super(QueryParamsController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def boolean_as_optional(self,
                            boolean,
                            boolean_1=None):
        """Does a GET request to /query/booleanAsOptional.

        TODO: type endpoint description here.

        Args:
            boolean (bool): TODO: type description here. Example: 
            boolean_1 (bool, optional): TODO: type description here. Example:
                
        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('boolean_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for boolean_as_optional.')
            self.validate_parameters(boolean=boolean)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for boolean_as_optional.')
            _url_path = '/query/booleanAsOptional'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'boolean': boolean,
                'boolean1': boolean_1
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for boolean_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for boolean_as_optional.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'boolean_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for boolean_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for boolean_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def rfc_1123_datetime_as_optional(self,
                                      date_time,
                                      date_time_1=None):
        """Does a GET request to /query/rfc1123dateTimeAsOptional.

        TODO: type endpoint description here.

        Args:
            date_time (datetime): TODO: type description here. Example: 
            date_time_1 (datetime, optional): TODO: type description here.
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
            self.logger.info('rfc_1123_datetime_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for rfc_1123_datetime_as_optional.')
            self.validate_parameters(date_time=date_time)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for rfc_1123_datetime_as_optional.')
            _url_path = '/query/rfc1123dateTimeAsOptional'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'dateTime': APIHelper.when_defined(APIHelper.HttpDateTime, date_time),
                'dateTime1': APIHelper.when_defined(APIHelper.HttpDateTime, date_time_1)
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for rfc_1123_datetime_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for rfc_1123_datetime_as_optional.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'rfc_1123_datetime_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for rfc_1123_datetime_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for rfc_1123_datetime_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def rfc_3339_datetime_as_optional(self,
                                      date_time,
                                      date_time_1=None):
        """Does a GET request to /query/rfc3339dateTimeAsOptional.

        TODO: type endpoint description here.

        Args:
            date_time (datetime): TODO: type description here. Example: 
            date_time_1 (datetime, optional): TODO: type description here.
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
            self.logger.info('rfc_3339_datetime_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for rfc_3339_datetime_as_optional.')
            self.validate_parameters(date_time=date_time)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for rfc_3339_datetime_as_optional.')
            _url_path = '/query/rfc3339dateTimeAsOptional'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'dateTime': APIHelper.when_defined(APIHelper.RFC3339DateTime, date_time),
                'dateTime1': APIHelper.when_defined(APIHelper.RFC3339DateTime, date_time_1)
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for rfc_3339_datetime_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for rfc_3339_datetime_as_optional.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'rfc_3339_datetime_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for rfc_3339_datetime_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for rfc_3339_datetime_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_date_as_optional(self,
                              date,
                              date_1=None):
        """Does a GET request to /query/dateAsOptional.

        TODO: type endpoint description here.

        Args:
            date (date): TODO: type description here. Example: 
            date_1 (date, optional): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_date_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_date_as_optional.')
            self.validate_parameters(date=date)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_date_as_optional.')
            _url_path = '/query/dateAsOptional'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'date': date,
                'date1': date_1
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_date_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_date_as_optional.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_date_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_date_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_date_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_string_as_optional(self,
                                string,
                                string_1=None):
        """Does a GET request to /query/stringAsOptional.

        TODO: type endpoint description here.

        Args:
            string (string): TODO: type description here. Example: 
            string_1 (string, optional): TODO: type description here. Example:
                
        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_string_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string_as_optional.')
            self.validate_parameters(string=string)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_as_optional.')
            _url_path = '/query/stringAsOptional'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'string': string,
                'string1': string_1
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_as_optional.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_string_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def unixdatetime_as_optional(self,
                                 date_time,
                                 date_time_1=None):
        """Does a GET request to /query/unixdateTimeAsOptional.

        TODO: type endpoint description here.

        Args:
            date_time (datetime): TODO: type description here. Example: 
            date_time_1 (datetime, optional): TODO: type description here.
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
            self.logger.info('unixdatetime_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for unixdatetime_as_optional.')
            self.validate_parameters(date_time=date_time)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for unixdatetime_as_optional.')
            _url_path = '/query/unixdateTimeAsOptional'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'dateTime': APIHelper.when_defined(APIHelper.UnixDateTime, date_time),
                'dateTime1': APIHelper.when_defined(APIHelper.UnixDateTime, date_time_1)
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for unixdatetime_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for unixdatetime_as_optional.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'unixdatetime_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for unixdatetime_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for unixdatetime_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_number_as_optional(self,
                                number,
                                number_1=None):
        """Does a GET request to /query/numberAsOptional.

        TODO: type endpoint description here.

        Args:
            number (int): TODO: type description here. Example: 
            number_1 (int, optional): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_number_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_number_as_optional.')
            self.validate_parameters(number=number)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_number_as_optional.')
            _url_path = '/query/numberAsOptional'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'number': number,
                'number1': number_1
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_number_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_number_as_optional.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_number_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_number_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_number_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_long_as_optional(self,
                              long,
                              long_1=None):
        """Does a GET request to /query/longAsOptional.

        TODO: type endpoint description here.

        Args:
            long (long|int): TODO: type description here. Example: 
            long_1 (long|int, optional): TODO: type description here. Example:
                
        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_long_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_long_as_optional.')
            self.validate_parameters(long=long)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_long_as_optional.')
            _url_path = '/query/longAsOptional'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'long': long,
                'long1': long_1
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_long_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_long_as_optional.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_long_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_long_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_long_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def precision_as_optional(self,
                              precision,
                              precision_1=None):
        """Does a GET request to /query/precisionAsOptional.

        TODO: type endpoint description here.

        Args:
            precision (float): TODO: type description here. Example: 
            precision_1 (float, optional): TODO: type description here.
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
            self.logger.info('precision_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for precision_as_optional.')
            self.validate_parameters(precision=precision)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for precision_as_optional.')
            _url_path = '/query/precisionAsOptional'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'precision': precision,
                'precision1': precision_1
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for precision_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for precision_as_optional.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'precision_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for precision_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for precision_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
