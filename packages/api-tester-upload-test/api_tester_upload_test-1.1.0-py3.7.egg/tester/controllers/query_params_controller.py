# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""

from tester.api_helper import APIHelper
from tester.configuration import Configuration
from tester.configuration import Server
from tester.controllers.base_controller import BaseController
from tester.models.server_response import ServerResponse


class QueryParamsController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, config, call_back=None):
        super(QueryParamsController, self).__init__(config, call_back)

    def send_number_as_optional(self,
                                number,
                                number_1=None):
        """Does a GET request to /query/numberAsOptional.

        TODO: type endpoint description here.

        Args:
            number (int): TODO: type description here.
            number_1 (int, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(number=number)

        # Prepare query URL
        _url_path = '/query/numberAsOptional'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'number': number,
            'number1': number_1
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters,
            self.config.array_serialization
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_long_as_optional(self,
                              long,
                              long_1=None):
        """Does a GET request to /query/longAsOptional.

        TODO: type endpoint description here.

        Args:
            long (long|int): TODO: type description here.
            long_1 (long|int, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(long=long)

        # Prepare query URL
        _url_path = '/query/longAsOptional'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'long': long,
            'long1': long_1
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters,
            self.config.array_serialization
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def precision_as_optional(self,
                              precision,
                              precision_1=None):
        """Does a GET request to /query/precisionAsOptional.

        TODO: type endpoint description here.

        Args:
            precision (float): TODO: type description here.
            precision_1 (float, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(precision=precision)

        # Prepare query URL
        _url_path = '/query/precisionAsOptional'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'precision': precision,
            'precision1': precision_1
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters,
            self.config.array_serialization
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def boolean_as_optional(self,
                            boolean,
                            boolean_1=None):
        """Does a GET request to /query/booleanAsOptional.

        TODO: type endpoint description here.

        Args:
            boolean (bool): TODO: type description here.
            boolean_1 (bool, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(boolean=boolean)

        # Prepare query URL
        _url_path = '/query/booleanAsOptional'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'boolean': boolean,
            'boolean1': boolean_1
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters,
            self.config.array_serialization
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def rfc_1123_datetime_as_optional(self,
                                      date_time,
                                      date_time_1=None):
        """Does a GET request to /query/rfc1123dateTimeAsOptional.

        TODO: type endpoint description here.

        Args:
            date_time (datetime): TODO: type description here.
            date_time_1 (datetime, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(date_time=date_time)

        # Prepare query URL
        _url_path = '/query/rfc1123dateTimeAsOptional'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'dateTime': APIHelper.when_defined(APIHelper.HttpDateTime, date_time),
            'dateTime1': APIHelper.when_defined(APIHelper.HttpDateTime, date_time_1)
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters,
            self.config.array_serialization
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def rfc_3339_datetime_as_optional(self,
                                      date_time,
                                      date_time_1=None):
        """Does a GET request to /query/rfc3339dateTimeAsOptional.

        TODO: type endpoint description here.

        Args:
            date_time (datetime): TODO: type description here.
            date_time_1 (datetime, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(date_time=date_time)

        # Prepare query URL
        _url_path = '/query/rfc3339dateTimeAsOptional'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'dateTime': APIHelper.when_defined(APIHelper.RFC3339DateTime, date_time),
            'dateTime1': APIHelper.when_defined(APIHelper.RFC3339DateTime, date_time_1)
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters,
            self.config.array_serialization
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_date_as_optional(self,
                              date,
                              date_1=None):
        """Does a GET request to /query/dateAsOptional.

        TODO: type endpoint description here.

        Args:
            date (date): TODO: type description here.
            date_1 (date, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(date=date)

        # Prepare query URL
        _url_path = '/query/dateAsOptional'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'date': date,
            'date1': date_1
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters,
            self.config.array_serialization
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_string_as_optional(self,
                                string,
                                string_1=None):
        """Does a GET request to /query/stringAsOptional.

        TODO: type endpoint description here.

        Args:
            string (string): TODO: type description here.
            string_1 (string, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(string=string)

        # Prepare query URL
        _url_path = '/query/stringAsOptional'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'string': string,
            'string1': string_1
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters,
            self.config.array_serialization
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def unixdatetime_as_optional(self,
                                 date_time,
                                 date_time_1=None):
        """Does a GET request to /query/unixdateTimeAsOptional.

        TODO: type endpoint description here.

        Args:
            date_time (datetime): TODO: type description here.
            date_time_1 (datetime, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(date_time=date_time)

        # Prepare query URL
        _url_path = '/query/unixdateTimeAsOptional'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'dateTime': APIHelper.when_defined(APIHelper.UnixDateTime, date_time),
            'dateTime1': APIHelper.when_defined(APIHelper.UnixDateTime, date_time_1)
        }
        _query_builder = APIHelper.append_url_with_query_parameters(
            _query_builder,
            _query_parameters,
            self.config.array_serialization
        )
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.get(_query_url, headers=_headers)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)
