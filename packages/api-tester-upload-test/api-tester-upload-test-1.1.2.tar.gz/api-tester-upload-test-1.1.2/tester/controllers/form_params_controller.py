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

class FormParamsController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, client=None, call_back=None):
        super(FormParamsController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def date_as_optional(self,
                         body):
        """Does a POST request to /form/optionalDateInModel.

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
            _url_path = '/form/optionalDateInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for date_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for date_as_optional.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for date_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/optionalDynamicInModel.

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
            _url_path = '/form/optionalDynamicInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for dynamic_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for dynamic_as_optional.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for dynamic_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/optionalStringInModel.

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
            _url_path = '/form/optionalStringInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for string_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for string_as_optional.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for string_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/optionalPrecisionInModel.

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
            _url_path = '/form/optionalPrecisionInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for precision_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for precision_as_optional.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for precision_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
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

    def long_as_optional(self,
                         body):
        """Does a POST request to /form/optionalLongInModel.

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
            _url_path = '/form/optionalLongInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for long_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for long_as_optional.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for long_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_number_as_optional(self,
                                body):
        """Does a POST request to /form/optionalNumberInModel.

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
            _url_path = '/form/optionalNumberInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_number_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_number_as_optional.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_number_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
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

    def send_datetime_optional_in_endpoint(self,
                                           body=None):
        """Does a POST request to /form/optionalDateTime.

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
            _url_path = '/form/optionalDateTime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_datetime_optional_in_endpoint.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_datetime_optional_in_endpoint.')
            _form_parameters = {
                'body': APIHelper.when_defined(APIHelper.RFC3339DateTime, body)
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_datetime_optional_in_endpoint.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/optionalUnixDateTimeInModel.

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
            _url_path = '/form/optionalUnixDateTimeInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_optional_unix_time_stamp_in_model_body.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_optional_unix_time_stamp_in_model_body.')
            _form_parameters = {
                'dateTime': date_time
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_optional_unix_time_stamp_in_model_body.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/optionalUnixTimeStampInNestedModel.

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
            _url_path = '/form/optionalUnixTimeStampInNestedModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_optional_unix_time_stamp_in_nested_model_body.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_optional_unix_time_stamp_in_nested_model_body.')
            _form_parameters = {
                'dateTime': date_time
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_optional_unix_time_stamp_in_nested_model_body.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/rfc1123InNestedModel.

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
            _url_path = '/form/rfc1123InNestedModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_1123_date_time_in_nested_model.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_rfc_1123_date_time_in_nested_model.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_1123_date_time_in_nested_model.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/OptionalRfc1123InModel.

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
            _url_path = '/form/OptionalRfc1123InModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_1123_date_time_in_model.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_rfc_1123_date_time_in_model.')
            _form_parameters = {
                'dateTime': date_time
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_1123_date_time_in_model.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_optional_datetime_in_model(self,
                                        body):
        """Does a POST request to /form/optionalDateTimeInBody.

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
            _url_path = '/form/optionalDateTimeInBody'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_optional_datetime_in_model.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_optional_datetime_in_model.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_optional_datetime_in_model.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/dateTimeInNestedModel.

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
            _url_path = '/form/dateTimeInNestedModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_339_date_time_in_nested_models.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_rfc_339_date_time_in_nested_models.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_339_date_time_in_nested_models.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/optionalUUIDInModel.

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
            _url_path = '/form/optionalUUIDInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for uuid_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for uuid_as_optional.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for uuid_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_optional_unix_date_time_in_body(self,
                                             date_time=None):
        """Does a POST request to /form/optionalUnixTimeStamp.

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
            _url_path = '/form/optionalUnixTimeStamp'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_optional_unix_date_time_in_body.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_optional_unix_date_time_in_body.')
            _form_parameters = {
                'dateTime': APIHelper.when_defined(APIHelper.UnixDateTime, date_time)
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_optional_unix_date_time_in_body.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/optionlRfc1123.

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
            _url_path = '/form/optionlRfc1123'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_optional_rfc_1123_in_body.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_optional_rfc_1123_in_body.')
            _form_parameters = {
                'body': APIHelper.when_defined(APIHelper.HttpDateTime, body)
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_optional_rfc_1123_in_body.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def boolean_as_optional(self,
                            body):
        """Does a POST request to /form/optionalBooleanInModel.

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
            _url_path = '/form/optionalBooleanInModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for boolean_as_optional.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for boolean_as_optional.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for boolean_as_optional.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
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

    def send_string_in_form_with_new_line(self,
                                          body):
        """Does a POST request to /form/stringEncoding.

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
            self.logger.info('send_string_in_form_with_new_line called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string_in_form_with_new_line.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_in_form_with_new_line.')
            _url_path = '/form/stringEncoding'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string_in_form_with_new_line.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_string_in_form_with_new_line.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_in_form_with_new_line.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_string_in_form_with_new_line')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string_in_form_with_new_line.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string_in_form_with_new_line. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_string_in_form_with_r(self,
                                   body):
        """Does a POST request to /form/stringEncoding.

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
            self.logger.info('send_string_in_form_with_r called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string_in_form_with_r.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_in_form_with_r.')
            _url_path = '/form/stringEncoding'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string_in_form_with_r.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_string_in_form_with_r.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_in_form_with_r.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_string_in_form_with_r')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string_in_form_with_r.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string_in_form_with_r. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_string_in_form_with_r_n(self,
                                     body):
        """Does a POST request to /form/stringEncoding.

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
            self.logger.info('send_string_in_form_with_r_n called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string_in_form_with_r_n.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_in_form_with_r_n.')
            _url_path = '/form/stringEncoding'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string_in_form_with_r_n.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_string_in_form_with_r_n.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_in_form_with_r_n.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_string_in_form_with_r_n')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_string_in_form_with_r_n.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_string_in_form_with_r_n. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def update_string_array_with_form(self,
                                      strings):
        """Does a PUT request to /form/updateString.

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
            self.logger.info('update_string_array_with_form called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for update_string_array_with_form.')
            self.validate_parameters(strings=strings)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for update_string_array_with_form.')
            _url_path = '/form/updateString'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for update_string_array_with_form.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for update_string_array_with_form.')
            _form_parameters = {
                'strings': strings
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for update_string_array_with_form.')
            _request = self.http_client.put(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'update_string_array_with_form')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for update_string_array_with_form.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for update_string_array_with_form. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_integer_enum_array(self,
                                suites):
        """Does a POST request to /form/integerenum.

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
            _url_path = '/form/integerenum'
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
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_integer_enum_array.')
            _form_parameters = {
                'suites': suites
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_integer_enum_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_string_enum_array(self,
                               days):
        """Does a POST request to /form/stringenum.

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
            _url_path = '/form/stringenum'
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
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_string_enum_array.')
            _form_parameters = {
                'days': days
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_enum_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_delete_form_with_model_array(self,
                                          models):
        """Does a DELETE request to /form/deleteForm1.

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
            self.logger.info('send_delete_form_with_model_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_delete_form_with_model_array.')
            self.validate_parameters(models=models)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_delete_form_with_model_array.')
            _url_path = '/form/deleteForm1'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_delete_form_with_model_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_delete_form_with_model_array.')
            _form_parameters = {
                'models': models
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_delete_form_with_model_array.')
            _request = self.http_client.delete(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_delete_form_with_model_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_delete_form_with_model_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_delete_form_with_model_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def update_model_array_with_form(self,
                                     models):
        """Does a PUT request to /form/updateModel.

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
            self.logger.info('update_model_array_with_form called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for update_model_array_with_form.')
            self.validate_parameters(models=models)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for update_model_array_with_form.')
            _url_path = '/form/updateModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'array': True
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for update_model_array_with_form.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for update_model_array_with_form.')
            _form_parameters = {
                'models': models
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for update_model_array_with_form.')
            _request = self.http_client.put(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'update_model_array_with_form')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for update_model_array_with_form.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for update_model_array_with_form. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def update_string_with_form(self,
                                value):
        """Does a PUT request to /form/updateString.

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
            self.logger.info('update_string_with_form called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for update_string_with_form.')
            self.validate_parameters(value=value)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for update_string_with_form.')
            _url_path = '/form/updateString'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for update_string_with_form.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for update_string_with_form.')
            _form_parameters = {
                'value': value
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for update_string_with_form.')
            _request = self.http_client.put(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'update_string_with_form')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for update_string_with_form.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for update_string_with_form. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_rfc_3339_date_time_array(self,
                                      datetimes):
        """Does a POST request to /form/rfc3339datetime.

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
            _url_path = '/form/rfc3339datetime'
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
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_rfc_3339_date_time_array.')
            _form_parameters = {
                'datetimes': [APIHelper.when_defined(APIHelper.RFC3339DateTime, element) for element in datetimes]
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_3339_date_time_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_mixed_array(self,
                         options=dict()):
        """Does a POST request to /form/mixed.

        Send a variety for form params. Returns file count and body params

        Args:
            options (dict, optional): Key-value pairs for any of the
                parameters to this API Endpoint. All parameters to the
                endpoint are supplied through the dictionary with their names
                being the key and their desired values being the value. A list
                of parameters that can be used are::

                    file -- string -- TODO: type description here. Example: 
                    integers -- list of int -- TODO: type description here.
                        Example: 
                    models -- list of Employee -- TODO: type description here.
                        Example: 
                    strings -- list of string -- TODO: type description here.
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
            self.logger.info('send_mixed_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_mixed_array.')
            self.validate_parameters(file=options.get("file"),
                                     integers=options.get("integers"),
                                     models=options.get("models"),
                                     strings=options.get("strings"))
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_mixed_array.')
            _url_path = '/form/mixed'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare files
            self.logger.info('Preparing files for send_mixed_array.')
            _files = {
                'file': options.get('file', None)
            }
    
            # Prepare headers
            self.logger.info('Preparing headers for send_mixed_array.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_mixed_array.')
            _form_parameters = {
                'integers': options.get('integers', None),
                'models': options.get('models', None),
                'strings': options.get('strings', None)
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_mixed_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters, files=_files)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_mixed_array')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_mixed_array.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_mixed_array. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def update_model_with_form(self,
                               model):
        """Does a PUT request to /form/updateModel.

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
            self.logger.info('update_model_with_form called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for update_model_with_form.')
            self.validate_parameters(model=model)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for update_model_with_form.')
            _url_path = '/form/updateModel'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for update_model_with_form.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for update_model_with_form.')
            _form_parameters = {
                'model': model
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for update_model_with_form.')
            _request = self.http_client.put(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'update_model_with_form')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for update_model_with_form.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for update_model_with_form. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_delete_form_1(self,
                           model):
        """Does a DELETE request to /form/deleteForm1.

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
            self.logger.info('send_delete_form_1 called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_delete_form_1.')
            self.validate_parameters(model=model)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_delete_form_1.')
            _url_path = '/form/deleteForm1'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_delete_form_1.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_delete_form_1.')
            _form_parameters = {
                'model': model
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_delete_form_1.')
            _request = self.http_client.delete(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_delete_form_1')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_delete_form_1.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_delete_form_1. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_integer_array(self,
                           integers):
        """Does a POST request to /form/number.

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
            _url_path = '/form/number'
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
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_integer_array.')
            _form_parameters = {
                'integers': integers
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_integer_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_string_array(self,
                          strings):
        """Does a POST request to /form/string.

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
            self.logger.info('send_string_array called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_string_array.')
            self.validate_parameters(strings=strings)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_string_array.')
            _url_path = '/form/string'
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
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_string_array.')
            _form_parameters = {
                'strings': strings
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def allow_dynamic_form_fields(self,
                                  name,
                                  _optional_form_parameters=None):
        """Does a POST request to /form/allowDynamicFormFields.

        TODO: type endpoint description here.

        Args:
            name (string): TODO: type description here. Example: 
            _optional_form_parameters (Array, optional): Additional optional
                form parameters are supported by this endpoint

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('allow_dynamic_form_fields called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for allow_dynamic_form_fields.')
            self.validate_parameters(name=name)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for allow_dynamic_form_fields.')
            _url_path = '/form/allowDynamicFormFields'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for allow_dynamic_form_fields.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for allow_dynamic_form_fields.')
            _form_parameters = {
                'name': name
            }
            if _form_parameters != None and _optional_form_parameters != None:
                _form_parameters.update(APIHelper.form_encode_parameters(_optional_form_parameters,
                    Configuration.array_serialization))
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for allow_dynamic_form_fields.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'allow_dynamic_form_fields')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for allow_dynamic_form_fields.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for allow_dynamic_form_fields. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_model_array(self,
                         models):
        """Does a POST request to /form/model.

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
            _url_path = '/form/model'
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
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_model_array.')
            _form_parameters = {
                'models': models
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_model_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_file(self,
                  file):
        """Does a POST request to /form/file.

        TODO: type endpoint description here.

        Args:
            file (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_file called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_file.')
            self.validate_parameters(file=file)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_file.')
            _url_path = '/form/file'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare files
            self.logger.info('Preparing files for send_file.')
            _files = {
                'file': file
            }
    
            # Prepare headers
            self.logger.info('Preparing headers for send_file.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_file.')
            _request = self.http_client.post(_query_url, headers=_headers, files=_files)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_file')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_file.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_file. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_multiple_files(self,
                            file,
                            file_1):
        """Does a POST request to /form/multipleFiles.

        TODO: type endpoint description here.

        Args:
            file (string): TODO: type description here. Example: 
            file_1 (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_multiple_files called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_multiple_files.')
            self.validate_parameters(file=file,
                                     file_1=file_1)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_multiple_files.')
            _url_path = '/form/multipleFiles'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare files
            self.logger.info('Preparing files for send_multiple_files.')
            _files = {
                'file': file,
                'file1': file_1
            }
    
            # Prepare headers
            self.logger.info('Preparing headers for send_multiple_files.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_multiple_files.')
            _request = self.http_client.post(_query_url, headers=_headers, files=_files)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_multiple_files')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_multiple_files.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_multiple_files. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_string(self,
                    value):
        """Does a POST request to /form/string.

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
            _url_path = '/form/string'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_string.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_string.')
            _form_parameters = {
                'value': value
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_string.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_long(self,
                  value):
        """Does a POST request to /form/number.

        TODO: type endpoint description here.

        Args:
            value (long|int): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_long called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_long.')
            self.validate_parameters(value=value)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_long.')
            _url_path = '/form/number'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_long.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_long.')
            _form_parameters = {
                'value': value
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_long.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_long')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_long.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_long. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_model(self,
                   model):
        """Does a POST request to /form/model.

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
            _url_path = '/form/model'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_model.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_model.')
            _form_parameters = {
                'model': model
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_model.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_unix_date_time_array(self,
                                  datetimes):
        """Does a POST request to /form/unixdatetime.

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
            _url_path = '/form/unixdatetime'
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
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_unix_date_time_array.')
            _form_parameters = {
                'datetimes': [APIHelper.when_defined(APIHelper.UnixDateTime, element) for element in datetimes]
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_unix_date_time_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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
        """Does a POST request to /form/rfc1123datetime.

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
            _url_path = '/form/rfc1123datetime'
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
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_rfc_1123_date_time_array.')
            _form_parameters = {
                'datetimes': [APIHelper.when_defined(APIHelper.HttpDateTime, element) for element in datetimes]
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_1123_date_time_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_rfc_1123_date_time(self,
                                datetime):
        """Does a POST request to /form/rfc1123datetime.

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
            _url_path = '/form/rfc1123datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_1123_date_time.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_rfc_1123_date_time.')
            _form_parameters = {
                'datetime': APIHelper.when_defined(APIHelper.HttpDateTime, datetime)
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_1123_date_time.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_rfc_3339_date_time(self,
                                datetime):
        """Does a POST request to /form/rfc3339datetime.

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
            _url_path = '/form/rfc3339datetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_rfc_3339_date_time.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_rfc_3339_date_time.')
            _form_parameters = {
                'datetime': APIHelper.when_defined(APIHelper.RFC3339DateTime, datetime)
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_rfc_3339_date_time.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_date_array(self,
                        dates):
        """Does a POST request to /form/date.

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
            _url_path = '/form/date'
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
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_date_array.')
            _form_parameters = {
                'dates': dates
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_date_array.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_date(self,
                  date):
        """Does a POST request to /form/date.

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
            _url_path = '/form/date'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_date.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_date.')
            _form_parameters = {
                'date': date
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_date.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_unix_date_time(self,
                            datetime):
        """Does a POST request to /form/unixdatetime.

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
            _url_path = '/form/unixdatetime'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_unix_date_time.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_unix_date_time.')
            _form_parameters = {
                'datetime': APIHelper.when_defined(APIHelper.UnixDateTime, datetime)
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_unix_date_time.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
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

    def send_delete_multipart(self,
                              file):
        """Does a DELETE request to /form/deleteMultipart.

        TODO: type endpoint description here.

        Args:
            file (string): TODO: type description here. Example: 

        Returns:
            ServerResponse: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('send_delete_multipart called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_delete_multipart.')
            self.validate_parameters(file=file)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_delete_multipart.')
            _url_path = '/form/deleteMultipart'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare files
            self.logger.info('Preparing files for send_delete_multipart.')
            _files = {
                'file': file
            }
    
            # Prepare headers
            self.logger.info('Preparing headers for send_delete_multipart.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_delete_multipart.')
            _request = self.http_client.delete(_query_url, headers=_headers, files=_files)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_delete_multipart')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_delete_multipart.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_delete_multipart. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def send_delete_form(self,
                         body):
        """Does a DELETE request to /form/deleteForm.

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
            self.logger.info('send_delete_form called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for send_delete_form.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for send_delete_form.')
            _url_path = '/form/deleteForm'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for send_delete_form.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare form parameters
            self.logger.info('Preparing form parameters for send_delete_form.')
            _form_parameters = {
                'body': body
            }
            _form_parameters = APIHelper.form_encode_parameters(_form_parameters,
                Configuration.array_serialization)
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for send_delete_form.')
            _request = self.http_client.delete(_query_url, headers=_headers, parameters=_form_parameters)
            AuthManager.apply(_request, _url_path)
            _context = self.execute_request(_request, name = 'send_delete_form')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for send_delete_form.')
            if _context.response.status_code == 404:
                self.logger.info('Status code 404 received for send_delete_form. Returning nil.')
                return None
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
