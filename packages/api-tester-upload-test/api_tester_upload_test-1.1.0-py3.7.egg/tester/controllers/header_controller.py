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


class HeaderController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, config, call_back=None):
        super(HeaderController, self).__init__(config, call_back)

    def send_headers(self,
                     custom_header,
                     value):
        """Does a POST request to /header.

        Sends a single header params

        Args:
            custom_header (string): TODO: type description here.
            value (string): Represents the value of the custom header

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(custom_header=custom_header,
                                 value=value)

        # Prepare query URL
        _url_path = '/header'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json',
            'custom-header': custom_header
        }

        # Prepare form parameters
        _form_parameters = {
            'value': value
        }

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)
