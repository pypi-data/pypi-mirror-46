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

class BodyParamsController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, client=None, call_back=None):
        super(BodyParamsController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def send_number_as_optional(self,
                                body):
        """Does a POST request to /body/optionalNumberInModel.

        TODO: type endpoint description here.

        Args:
            body (NumberAsOptional): TODO: type description here. Example: 

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
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_number_as_optional.')
            _url_path = '/body/optionalNumberInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_number_as_optional.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_number_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
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

    def send_optional_datetime_in_model(self,
                                        body):
        """Does a POST request to /body/optionalDateTimeInBody.

        TODO: type endpoint description here.

        Args:
            body (ModelWithOptionalRfc3339DateTime): TODO: type description
                here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_optional_datetime_in_model called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_optional_datetime_in_model.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_optional_datetime_in_model.')
            _url_path = '/body/optionalDateTimeInBody'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_optional_datetime_in_model.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_optional_datetime_in_model.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'send_optional_datetime_in_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_optional_datetime_in_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_optional_datetime_in_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_rfc_339_date_time_in_nested_models(self,
                                                body):
        """Does a POST request to /body/dateTimeInNestedModel.

        TODO: type endpoint description here.

        Args:
            body (SendRfc339DateTime): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_rfc_339_date_time_in_nested_models called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_rfc_339_date_time_in_nested_models.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_rfc_339_date_time_in_nested_models.')
            _url_path = '/body/dateTimeInNestedModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_339_date_time_in_nested_models.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_339_date_time_in_nested_models.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'send_rfc_339_date_time_in_nested_models')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_rfc_339_date_time_in_nested_models.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_rfc_339_date_time_in_nested_models. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def uuid_as_optional(self,
                         body):
        """Does a POST request to /body/optionalUUIDInModel.

        TODO: type endpoint description here.

        Args:
            body (UuidAsOptional): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('uuid_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for uuid_as_optional.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for uuid_as_optional.')
            _url_path = '/body/optionalUUIDInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for uuid_as_optional.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for uuid_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'uuid_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for uuid_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for uuid_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def date_as_optional(self,
                         body):
        """Does a POST request to /body/optionalDateInModel.

        TODO: type endpoint description here.

        Args:
            body (DateAsOptional): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('date_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for date_as_optional.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for date_as_optional.')
            _url_path = '/body/optionalDateInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for date_as_optional.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for date_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'date_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for date_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for date_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def dynamic_as_optional(self,
                            body):
        """Does a POST request to /body/optionalDynamicInModel.

        TODO: type endpoint description here.

        Args:
            body (DynamicAsOptional): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('dynamic_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for dynamic_as_optional.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for dynamic_as_optional.')
            _url_path = '/body/optionalDynamicInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for dynamic_as_optional.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for dynamic_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'dynamic_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for dynamic_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for dynamic_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def string_as_optional(self,
                           body):
        """Does a POST request to /body/optionalStringInModel.

        TODO: type endpoint description here.

        Args:
            body (StringAsOptional): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('string_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for string_as_optional.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for string_as_optional.')
            _url_path = '/body/optionalStringInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for string_as_optional.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for string_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'string_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for string_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for string_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def precision_as_optional(self,
                              body):
        """Does a POST request to /body/optionalPrecisionInModel.

        TODO: type endpoint description here.

        Args:
            body (PrecisionAsOptional): TODO: type description here. Example:
                
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
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for precision_as_optional.')
            _url_path = '/body/optionalPrecisionInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for precision_as_optional.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for precision_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
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

    def long_as_optional(self,
                         body):
        """Does a POST request to /body/optionalLongInModel.

        TODO: type endpoint description here.

        Args:
            body (LongAsOptional): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('long_as_optional called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for long_as_optional.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for long_as_optional.')
            _url_path = '/body/optionalLongInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for long_as_optional.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for long_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'long_as_optional')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for long_as_optional.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for long_as_optional. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_optional_unix_date_time_in_body(self,
                                             date_time=None):
        """Does a POST request to /body/optionalUnixTimeStamp.

        TODO: type endpoint description here.

        Args:
            date_time (datetime, optional): TODO: type description here.
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
            self.logger.info('send_optional_unix_date_time_in_body called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_optional_unix_date_time_in_body.')
            _url_path = '/body/optionalUnixTimeStamp'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_optional_unix_date_time_in_body.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_optional_unix_date_time_in_body.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=str(APIHelper.when_defined(APIHelper.UnixDateTime,date_time)))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(date_time))
            _context = self.execute_request(_request, name = 'send_optional_unix_date_time_in_body')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_optional_unix_date_time_in_body.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_optional_unix_date_time_in_body. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_optional_rfc_1123_in_body(self,
                                       body):
        """Does a POST request to /body/optionlRfc1123.

        TODO: type endpoint description here.

        Args:
            body (datetime): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_optional_rfc_1123_in_body called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_optional_rfc_1123_in_body.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_optional_rfc_1123_in_body.')
            _url_path = '/body/optionlRfc1123'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_optional_rfc_1123_in_body.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_optional_rfc_1123_in_body.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=str(APIHelper.when_defined(APIHelper.HttpDateTime,body)))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'send_optional_rfc_1123_in_body')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_optional_rfc_1123_in_body.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_optional_rfc_1123_in_body. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_datetime_optional_in_endpoint(self,
                                           body=None):
        """Does a POST request to /body/optionalDateTime.

        TODO: type endpoint description here.

        Args:
            body (datetime, optional): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_datetime_optional_in_endpoint called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_datetime_optional_in_endpoint.')
            _url_path = '/body/optionalDateTime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_datetime_optional_in_endpoint.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_datetime_optional_in_endpoint.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=str(APIHelper.when_defined(APIHelper.RFC3339DateTime,body)))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'send_datetime_optional_in_endpoint')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_datetime_optional_in_endpoint.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_datetime_optional_in_endpoint. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_optional_unix_time_stamp_in_model_body(self,
                                                    date_time):
        """Does a POST request to /body/optionalUnixDateTimeInModel.

        TODO: type endpoint description here.

        Args:
            date_time (UnixDateTime): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_optional_unix_time_stamp_in_model_body called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_optional_unix_time_stamp_in_model_body.')
            self.validate_parameters(date_time=date_time)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_optional_unix_time_stamp_in_model_body.')
            _url_path = '/body/optionalUnixDateTimeInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_optional_unix_time_stamp_in_model_body.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_optional_unix_time_stamp_in_model_body.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(date_time))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(date_time))
            _context = self.execute_request(_request, name = 'send_optional_unix_time_stamp_in_model_body')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_optional_unix_time_stamp_in_model_body.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_optional_unix_time_stamp_in_model_body. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_optional_unix_time_stamp_in_nested_model_body(self,
                                                           date_time):
        """Does a POST request to /body/optionalUnixTimeStampInNestedModel.

        TODO: type endpoint description here.

        Args:
            date_time (SendUnixDateTime): TODO: type description here.
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
            self.logger.info('send_optional_unix_time_stamp_in_nested_model_body called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_optional_unix_time_stamp_in_nested_model_body.')
            self.validate_parameters(date_time=date_time)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_optional_unix_time_stamp_in_nested_model_body.')
            _url_path = '/body/optionalUnixTimeStampInNestedModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_optional_unix_time_stamp_in_nested_model_body.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_optional_unix_time_stamp_in_nested_model_body.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(date_time))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(date_time))
            _context = self.execute_request(_request, name = 'send_optional_unix_time_stamp_in_nested_model_body')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_optional_unix_time_stamp_in_nested_model_body.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_optional_unix_time_stamp_in_nested_model_body. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_rfc_1123_date_time_in_nested_model(self,
                                                body):
        """Does a POST request to /body/rfc1123InNestedModel.

        TODO: type endpoint description here.

        Args:
            body (SendRfc1123DateTime): TODO: type description here. Example:
                
        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_rfc_1123_date_time_in_nested_model called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_rfc_1123_date_time_in_nested_model.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_rfc_1123_date_time_in_nested_model.')
            _url_path = '/body/rfc1123InNestedModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_1123_date_time_in_nested_model.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_1123_date_time_in_nested_model.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'send_rfc_1123_date_time_in_nested_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_rfc_1123_date_time_in_nested_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_rfc_1123_date_time_in_nested_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_rfc_1123_date_time_in_model(self,
                                         date_time):
        """Does a POST request to /body/OptionalRfc1123InModel.

        TODO: type endpoint description here.

        Args:
            date_time (ModelWithOptionalRfc1123DateTime): TODO: type
                description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_rfc_1123_date_time_in_model called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_rfc_1123_date_time_in_model.')
            self.validate_parameters(date_time=date_time)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_rfc_1123_date_time_in_model.')
            _url_path = '/body/OptionalRfc1123InModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_1123_date_time_in_model.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_1123_date_time_in_model.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(date_time))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(date_time))
            _context = self.execute_request(_request, name = 'send_rfc_1123_date_time_in_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_rfc_1123_date_time_in_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_rfc_1123_date_time_in_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def boolean_as_optional(self,
                            body):
        """Does a POST request to /body/optionalBooleanInModel.

        TODO: type endpoint description here.

        Args:
            body (BooleanAsOptional): TODO: type description here. Example: 

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
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for boolean_as_optional.')
            _url_path = '/body/optionalBooleanInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for boolean_as_optional.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for boolean_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
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

    def send_string_with_new_line(self,
                                  body):
        """Does a POST request to /body/stringEncoding.

        TODO: type endpoint description here.

        Args:
            body (TestNstringEncoding): TODO: type description here. Example:
                
        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_string_with_new_line called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string_with_new_line.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_with_new_line.')
            _url_path = '/body/stringEncoding'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string_with_new_line.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_with_new_line.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'send_string_with_new_line')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string_with_new_line.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string_with_new_line. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_string_with_r(self,
                           body):
        """Does a POST request to /body/stringEncoding.

        TODO: type endpoint description here.

        Args:
            body (TestRstringEncoding): TODO: type description here. Example:
                
        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_string_with_r called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string_with_r.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_with_r.')
            _url_path = '/body/stringEncoding'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string_with_r.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_with_r.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'send_string_with_r')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string_with_r.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string_with_r. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_string_in_body_with_r_n(self,
                                     body):
        """Does a POST request to /body/stringEncoding.

        TODO: type endpoint description here.

        Args:
            body (TestRNstringEncoding): TODO: type description here. Example:
                
        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_string_in_body_with_r_n called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string_in_body_with_r_n.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_in_body_with_r_n.')
            _url_path = '/body/stringEncoding'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string_in_body_with_r_n.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_in_body_with_r_n.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'send_string_in_body_with_r_n')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string_in_body_with_r_n.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string_in_body_with_r_n. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_delete_body_with_model(self,
                                    model):
        """Does a DELETE request to /body/deleteBody1.

        TODO: type endpoint description here.

        Args:
            model (Employee): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_delete_body_with_model called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_delete_body_with_model.')
            self.validate_parameters(model=model)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_delete_body_with_model.')
            _url_path = '/body/deleteBody1'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_delete_body_with_model.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_delete_body_with_model.')
            _request = self.http_client.delete(_query_url, headers=_headers, parameters=APIHelper.json_serialize(model))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(model))
            _context = self.execute_request(_request, name = 'send_delete_body_with_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_delete_body_with_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_delete_body_with_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_delete_body_with_model_array(self,
                                          models):
        """Does a DELETE request to /body/deleteBody1.

        TODO: type endpoint description here.

        Args:
            models (list of Employee): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_delete_body_with_model_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_delete_body_with_model_array.')
            self.validate_parameters(models=models)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_delete_body_with_model_array.')
            _url_path = '/body/deleteBody1'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_delete_body_with_model_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_delete_body_with_model_array.')
            _request = self.http_client.delete(_query_url, headers=_headers, parameters=APIHelper.json_serialize(models))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(models))
            _context = self.execute_request(_request, name = 'send_delete_body_with_model_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_delete_body_with_model_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_delete_body_with_model_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def update_model_array(self,
                           models):
        """Does a PUT request to /body/updateModel.

        TODO: type endpoint description here.

        Args:
            models (list of Employee): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('update_model_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for update_model_array.')
            self.validate_parameters(models=models)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for update_model_array.')
            _url_path = '/body/updateModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for update_model_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for update_model_array.')
            _request = self.http_client.put(_query_url, headers=_headers, parameters=APIHelper.json_serialize(models))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(models))
            _context = self.execute_request(_request, name = 'update_model_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for update_model_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for update_model_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def update_string_1(self,
                        value):
        """Does a PUT request to /body/updateString.

        TODO: type endpoint description here.

        Args:
            value (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('update_string_1 called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for update_string_1.')
            self.validate_parameters(value=value)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for update_string_1.')
            _url_path = '/body/updateString'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for update_string_1.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for update_string_1.')
            _request = self.http_client.put(_query_url, headers=_headers, parameters=value)
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(value))
            _context = self.execute_request(_request, name = 'update_string_1')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for update_string_1.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for update_string_1. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def update_string_array(self,
                            strings):
        """Does a PUT request to /body/updateString.

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
            self.logger.info('update_string_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for update_string_array.')
            self.validate_parameters(strings=strings)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for update_string_array.')
            _url_path = '/body/updateString'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for update_string_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for update_string_array.')
            _request = self.http_client.put(_query_url, headers=_headers, parameters=APIHelper.json_serialize(strings))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(strings))
            _context = self.execute_request(_request, name = 'update_string_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for update_string_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for update_string_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_string_enum_array(self,
                               days):
        """Does a POST request to /body/stringenum.

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
            self.logger.info('send_string_enum_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string_enum_array.')
            self.validate_parameters(days=days)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_enum_array.')
            _url_path = '/body/stringenum'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string_enum_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_enum_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(days))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(days))
            _context = self.execute_request(_request, name = 'send_string_enum_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string_enum_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string_enum_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_integer_enum_array(self,
                                suites):
        """Does a POST request to /body/integerenum.

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
            self.logger.info('send_integer_enum_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_integer_enum_array.')
            self.validate_parameters(suites=suites)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_integer_enum_array.')
            _url_path = '/body/integerenum'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_integer_enum_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_integer_enum_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(suites))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(suites))
            _context = self.execute_request(_request, name = 'send_integer_enum_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_integer_enum_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_integer_enum_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def update_model(self,
                     model):
        """Does a PUT request to /body/updateModel.

        TODO: type endpoint description here.

        Args:
            model (Employee): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('update_model called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for update_model.')
            self.validate_parameters(model=model)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for update_model.')
            _url_path = '/body/updateModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for update_model.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for update_model.')
            _request = self.http_client.put(_query_url, headers=_headers, parameters=APIHelper.json_serialize(model))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(model))
            _context = self.execute_request(_request, name = 'update_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for update_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for update_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_string(self,
                    value):
        """Does a POST request to /body/string.

        TODO: type endpoint description here.

        Args:
            value (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_string called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string.')
            self.validate_parameters(value=value)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string.')
            _url_path = '/body/string'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=value)
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(value))
            _context = self.execute_request(_request, name = 'send_string')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def update_string(self,
                      value):
        """Does a PUT request to /body/updateString.

        TODO: type endpoint description here.

        Args:
            value (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('update_string called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for update_string.')
            self.validate_parameters(value=value)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for update_string.')
            _url_path = '/body/updateString'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for update_string.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for update_string.')
            _request = self.http_client.put(_query_url, headers=_headers, parameters=value)
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(value))
            _context = self.execute_request(_request, name = 'update_string')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for update_string.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for update_string. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_integer_array(self,
                           integers):
        """Does a POST request to /body/number.

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
            self.logger.info('send_integer_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_integer_array.')
            self.validate_parameters(integers=integers)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_integer_array.')
            _url_path = '/body/number'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_integer_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_integer_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(integers))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(integers))
            _context = self.execute_request(_request, name = 'send_integer_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_integer_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_integer_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def wrap_body_in_object(self,
                            field,
                            name):
        """Does a POST request to /body/wrapParamInObject.

        TODO: type endpoint description here.

        Args:
            field (string): TODO: type description here. Example: 
            name (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('wrap_body_in_object called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for wrap_body_in_object.')
            self.validate_parameters(field=field,
                                     name=name)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for wrap_body_in_object.')
            _url_path = '/body/wrapParamInObject'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for wrap_body_in_object.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare wrapper object for body parameters
            self.logger.info('Preparing body parameters for wrap_body_in_object.')
            _body_parameters = {
                'field': field,
                'name': name
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for wrap_body_in_object.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(_body_parameters))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(field))
            _context = self.execute_request(_request, name = 'wrap_body_in_object')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for wrap_body_in_object.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for wrap_body_in_object. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def validate_required_parameter(self,
                                    model,
                                    option=None):
        """Does a POST request to /body/validateRequiredParam.

        TODO: type endpoint description here.

        Args:
            model (Validate): TODO: type description here. Example: 
            option (string, optional): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('validate_required_parameter called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for validate_required_parameter.')
            self.validate_parameters(model=model)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for validate_required_parameter.')
            _url_path = '/body/validateRequiredParam'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'option': option
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for validate_required_parameter.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for validate_required_parameter.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(model))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(model))
            _context = self.execute_request(_request, name = 'validate_required_parameter')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for validate_required_parameter.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for validate_required_parameter. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def additional_model_parameters_1(self,
                                      model):
        """Does a POST request to /body/additionalModelProperties.

        TODO: type endpoint description here.

        Args:
            model (AdditionalModelParameters): TODO: type description here.
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
            self.logger.info('additional_model_parameters_1 called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for additional_model_parameters_1.')
            self.validate_parameters(model=model)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for additional_model_parameters_1.')
            _url_path = '/body/additionalModelProperties'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for additional_model_parameters_1.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for additional_model_parameters_1.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(model))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(model))
            _context = self.execute_request(_request, name = 'additional_model_parameters_1')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for additional_model_parameters_1.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for additional_model_parameters_1. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_model(self,
                   model):
        """Does a POST request to /body/model.

        TODO: type endpoint description here.

        Args:
            model (Employee): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_model called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_model.')
            self.validate_parameters(model=model)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_model.')
            _url_path = '/body/model'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_model.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_model.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(model))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(model))
            _context = self.execute_request(_request, name = 'send_model')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_model.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_model. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_model_array(self,
                         models):
        """Does a POST request to /body/model.

        TODO: type endpoint description here.

        Args:
            models (list of Employee): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_model_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_model_array.')
            self.validate_parameters(models=models)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_model_array.')
            _url_path = '/body/model'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_model_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_model_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(models))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(models))
            _context = self.execute_request(_request, name = 'send_model_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_model_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_model_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_dynamic(self,
                     dynamic):
        """Does a POST request to /body/dynamic.

        TODO: type endpoint description here.

        Args:
            dynamic (object): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_dynamic called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_dynamic.')
            self.validate_parameters(dynamic=dynamic)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_dynamic.')
            _url_path = '/body/dynamic'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_dynamic.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_dynamic.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(dynamic))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(dynamic))
            _context = self.execute_request(_request, name = 'send_dynamic')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_dynamic.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_dynamic. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_rfc_3339_date_time_array(self,
                                      datetimes):
        """Does a POST request to /body/rfc3339datetime.

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
            self.logger.info('send_rfc_3339_date_time_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_rfc_3339_date_time_array.')
            self.validate_parameters(datetimes=datetimes)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_rfc_3339_date_time_array.')
            _url_path = '/body/rfc3339datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_3339_date_time_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_3339_date_time_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize([APIHelper.when_defined(APIHelper.RFC3339DateTime,element) for element in datetimes]))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(datetimes))
            _context = self.execute_request(_request, name = 'send_rfc_3339_date_time_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_rfc_3339_date_time_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_rfc_3339_date_time_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_string_array(self,
                          sarray):
        """Does a POST request to /body/string.

        sends a string body param

        Args:
            sarray (list of string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

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
            self.validate_parameters(sarray=sarray)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_array.')
            _url_path = '/body/string'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(sarray))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(sarray))
            _context = self.execute_request(_request, name = 'send_string_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def additional_model_parameters(self,
                                    model):
        """Does a POST request to /body/additionalModelProperties.

        TODO: type endpoint description here.

        Args:
            model (AdditionalModelParameters): TODO: type description here.
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
            self.logger.info('additional_model_parameters called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for additional_model_parameters.')
            self.validate_parameters(model=model)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for additional_model_parameters.')
            _url_path = '/body/additionalModelProperties'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for additional_model_parameters.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for additional_model_parameters.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(model))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(model))
            _context = self.execute_request(_request, name = 'additional_model_parameters')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for additional_model_parameters.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for additional_model_parameters. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_unix_date_time_array(self,
                                  datetimes):
        """Does a POST request to /body/unixdatetime.

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
            self.logger.info('send_unix_date_time_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_unix_date_time_array.')
            self.validate_parameters(datetimes=datetimes)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_unix_date_time_array.')
            _url_path = '/body/unixdatetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_unix_date_time_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_unix_date_time_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize([APIHelper.when_defined(APIHelper.UnixDateTime,element) for element in datetimes]))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(datetimes))
            _context = self.execute_request(_request, name = 'send_unix_date_time_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_unix_date_time_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_unix_date_time_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_rfc_1123_date_time_array(self,
                                      datetimes):
        """Does a POST request to /body/rfc1123datetime.

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
            self.logger.info('send_rfc_1123_date_time_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_rfc_1123_date_time_array.')
            self.validate_parameters(datetimes=datetimes)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_rfc_1123_date_time_array.')
            _url_path = '/body/rfc1123datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_1123_date_time_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_1123_date_time_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize([APIHelper.when_defined(APIHelper.HttpDateTime,element) for element in datetimes]))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(datetimes))
            _context = self.execute_request(_request, name = 'send_rfc_1123_date_time_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_rfc_1123_date_time_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_rfc_1123_date_time_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_delete_plain_text(self,
                               text_string):
        """Does a DELETE request to /body/deletePlainTextBody.

        TODO: type endpoint description here.

        Args:
            text_string (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_delete_plain_text called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_delete_plain_text.')
            self.validate_parameters(text_string=text_string)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_delete_plain_text.')
            _url_path = '/body/deletePlainTextBody'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_delete_plain_text.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_delete_plain_text.')
            _request = self.http_client.delete(_query_url, headers=_headers, parameters=text_string)
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(text_string))
            _context = self.execute_request(_request, name = 'send_delete_plain_text')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_delete_plain_text.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_delete_plain_text. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_date_array(self,
                        dates):
        """Does a POST request to /body/date.

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
            self.logger.info('send_date_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_date_array.')
            self.validate_parameters(dates=dates)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_date_array.')
            _url_path = '/body/date'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_date_array.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_date_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(dates))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(dates))
            _context = self.execute_request(_request, name = 'send_date_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_date_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_date_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_rfc_3339_date_time(self,
                                datetime):
        """Does a POST request to /body/rfc3339datetime.

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
            self.logger.info('send_rfc_3339_date_time called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_rfc_3339_date_time.')
            self.validate_parameters(datetime=datetime)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_rfc_3339_date_time.')
            _url_path = '/body/rfc3339datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_3339_date_time.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_3339_date_time.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=str(APIHelper.when_defined(APIHelper.RFC3339DateTime,datetime)))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(datetime))
            _context = self.execute_request(_request, name = 'send_rfc_3339_date_time')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_rfc_3339_date_time.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_rfc_3339_date_time. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_rfc_1123_date_time(self,
                                datetime):
        """Does a POST request to /body/rfc1123datetime.

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
            self.logger.info('send_rfc_1123_date_time called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_rfc_1123_date_time.')
            self.validate_parameters(datetime=datetime)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_rfc_1123_date_time.')
            _url_path = '/body/rfc1123datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_1123_date_time.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_1123_date_time.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=str(APIHelper.when_defined(APIHelper.HttpDateTime,datetime)))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(datetime))
            _context = self.execute_request(_request, name = 'send_rfc_1123_date_time')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_rfc_1123_date_time.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_rfc_1123_date_time. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_unix_date_time(self,
                            datetime):
        """Does a POST request to /body/unixdatetime.

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
            self.logger.info('send_unix_date_time called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_unix_date_time.')
            self.validate_parameters(datetime=datetime)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_unix_date_time.')
            _url_path = '/body/unixdatetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_unix_date_time.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_unix_date_time.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=str(APIHelper.when_defined(APIHelper.UnixDateTime,datetime)))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(datetime))
            _context = self.execute_request(_request, name = 'send_unix_date_time')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_unix_date_time.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_unix_date_time. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_date(self,
                  date):
        """Does a POST request to /body/date.

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
            self.logger.info('send_date called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_date.')
            self.validate_parameters(date=date)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_date.')
            _url_path = '/body/date'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_date.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'text/plain; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_date.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=str(date))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(date))
            _context = self.execute_request(_request, name = 'send_date')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_date.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_date. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_delete_body(self,
                         body):
        """Does a DELETE request to /body/deleteBody.

        TODO: type endpoint description here.

        Args:
            body (DeleteBody): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_delete_body called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_delete_body.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_delete_body.')
            _url_path = '/body/deleteBody'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_delete_body.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_delete_body.')
            _request = self.http_client.delete(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request, _url_path, APIHelper.json_serialize(body))
            _context = self.execute_request(_request, name = 'send_delete_body')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_delete_body.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_delete_body. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
