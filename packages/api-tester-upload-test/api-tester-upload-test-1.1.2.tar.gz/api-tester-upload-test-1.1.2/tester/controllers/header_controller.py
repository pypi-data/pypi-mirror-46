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

class HeaderController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, client=None, call_back=None):
        super(HeaderController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def send_headers(self,
                     custom_header,
                     value):
        """Does a POST request to /header.

        Sends a single header params

        Args:
            custom_header (string): TODO: type description here. Example: 
            value (string): Represents the value of the custom header

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_headers called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_headers.')
            self.validate_parameters(custom_header=custom_header,
                                     value=value)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_headers.')
            _url_path = '/header'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_headers.')
            _headers = {
                'accept': 'application/json',
                'custom-header': custom_header
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_headers.')
            _form_parameters = {
                'value': value
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_headers.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_headers')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_headers.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_headers. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_message(self,
                    operation):
        """Does a GET request to /{operation}.

        TODO: type endpoint description here.

        Args:
            operation (string): TODO: type description here. Example: 

        Returns:
            void: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_message called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for get_message.')
            self.validate_parameters(operation=operation)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_message.')
            _url_path = '/{operation}'
            _url_path = APIHelper.append_url_with_template_parameters(_url_path, { 
                'operation': operation
            })
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_message.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_message')
            self.validate_response(_context)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_message_1(self,
                      operation):
        """Does a GET request to /{operation}.

        TODO: type endpoint description here.

        Args:
            operation (string): TODO: type description here. Example: 

        Returns:
            void: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_message_1 called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for get_message_1.')
            self.validate_parameters(operation=operation)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_message_1.')
            _url_path = '/{operation}'
            _url_path = APIHelper.append_url_with_template_parameters(_url_path, { 
                'operation': operation
            })
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_message_1.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'get_message_1')
            self.validate_response(_context)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
