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
from tester.models.echo_response import EchoResponse


class TemplateParamsController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, config, call_back=None):
        super(TemplateParamsController, self).__init__(config, call_back)

    def send_string_array(self,
                          strings):
        """Does a GET request to /{strings}.

        TODO: type endpoint description here.

        Args:
            strings (list of string): TODO: type description here.

        Returns:
            EchoResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(strings=strings)

        # Prepare query URL
        _url_path = '/{strings}'
        _url_path = APIHelper.append_url_with_template_parameters(_url_path, {
            'strings': strings
        })
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
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
        return APIHelper.json_deserialize(_context.response.raw_body, EchoResponse.from_dictionary)

    def send_integer_array(self,
                           integers):
        """Does a GET request to /{integers}.

        TODO: type endpoint description here.

        Args:
            integers (list of int): TODO: type description here.

        Returns:
            EchoResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(integers=integers)

        # Prepare query URL
        _url_path = '/{integers}'
        _url_path = APIHelper.append_url_with_template_parameters(_url_path, {
            'integers': integers
        })
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
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
        return APIHelper.json_deserialize(_context.response.raw_body, EchoResponse.from_dictionary)
