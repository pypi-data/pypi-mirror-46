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
from tester.models.echo_response import EchoResponse

class TemplateParamsController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, client=None, call_back=None):
        super(TemplateParamsController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def send_string_array(self,
                          strings):
        """Does a GET request to /{strings}.

        TODO: type endpoint description here.

        Args:
            strings (list of string): TODO: type description here. Example: 

        Returns:
            EchoResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_string_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string_array.')
            self.validate_parameters(strings=strings)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_array.')
            _url_path = '/{strings}'
            _url_path = APIHelper.append_url_with_template_parameters(_url_path, { 
                'strings': strings
            })
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_string_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, EchoResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_integer_array(self,
                           integers):
        """Does a GET request to /{integers}.

        TODO: type endpoint description here.

        Args:
            integers (list of int): TODO: type description here. Example: 

        Returns:
            EchoResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_integer_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_integer_array.')
            self.validate_parameters(integers=integers)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_integer_array.')
            _url_path = '/{integers}'
            _url_path = APIHelper.append_url_with_template_parameters(_url_path, { 
                'integers': integers
            })
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_integer_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_integer_array.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_integer_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_integer_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_integer_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, EchoResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
