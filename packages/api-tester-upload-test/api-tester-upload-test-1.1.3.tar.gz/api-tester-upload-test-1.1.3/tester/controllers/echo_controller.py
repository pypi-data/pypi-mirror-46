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

class EchoController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, client=None, call_back=None):
        super(EchoController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def query_echo(self,
                   _optional_query_parameters=None):
        """Does a GET request to /.

        TODO: type endpoint description here.

        Args:
            _optional_form_parameters (Array, optional): Additional optional
                query parameters are supported by this endpoint

        Returns:
            EchoResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('query_echo called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for query_echo.')
            _url_path = '/'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _optional_query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for query_echo.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for query_echo.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'query_echo')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for query_echo.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for query_echo. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, EchoResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def json_echo(self,
                  input):
        """Does a POST request to /.

        Echo's back the request

        Args:
            input (object): TODO: type description here. Example: 

        Returns:
            mixed: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('json_echo called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for json_echo.')
            self.validate_parameters(input=input)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for json_echo.')
            _url_path = '/'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for json_echo.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for json_echo.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(input))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(input))
            _context = self.execute_request(_request, name = 'json_echo')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for json_echo.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for json_echo. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def form_echo(self,
                  input):
        """Does a POST request to /.

        Sends the request including any form params as JSON

        Args:
            input (object): TODO: type description here. Example: 

        Returns:
            mixed: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('form_echo called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for form_echo.')
            self.validate_parameters(input=input)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for form_echo.')
            _url_path = '/'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for form_echo.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for form_echo.')
            _form_parameters = {
                'input': input
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for form_echo.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'form_echo')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for form_echo.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for form_echo. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
