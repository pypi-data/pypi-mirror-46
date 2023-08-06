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


class FormParamsController(BaseController):

    """A Controller to access Endpoints in the tester API."""

    def __init__(self, config, call_back=None):
        super(FormParamsController, self).__init__(config, call_back)

    def send_delete_form(self,
                         body):
        """Does a DELETE request to /form/deleteForm.

        TODO: type endpoint description here.

        Args:
            body (DeleteBody): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/deleteForm'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.delete(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_delete_multipart(self,
                              file):
        """Does a DELETE request to /form/deleteMultipart.

        TODO: type endpoint description here.

        Args:
            file (string): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(file=file)

        # Prepare query URL
        _url_path = '/form/deleteMultipart'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare files
        _files = {
            'file': file
        }

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.delete(_query_url, headers=_headers, files=_files)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_date_array(self,
                        dates):
        """Does a POST request to /form/date.

        TODO: type endpoint description here.

        Args:
            dates (list of date): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(dates=dates)

        # Prepare query URL
        _url_path = '/form/date'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'dates': dates
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

    def send_date(self,
                  date):
        """Does a POST request to /form/date.

        TODO: type endpoint description here.

        Args:
            date (date): TODO: type description here.

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
        _url_path = '/form/date'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'date': date
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

    def send_unix_date_time(self,
                            datetime):
        """Does a POST request to /form/unixdatetime.

        TODO: type endpoint description here.

        Args:
            datetime (datetime): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(datetime=datetime)

        # Prepare query URL
        _url_path = '/form/unixdatetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'datetime': APIHelper.when_defined(APIHelper.UnixDateTime, datetime)
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

    def send_rfc_1123_date_time(self,
                                datetime):
        """Does a POST request to /form/rfc1123datetime.

        TODO: type endpoint description here.

        Args:
            datetime (datetime): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(datetime=datetime)

        # Prepare query URL
        _url_path = '/form/rfc1123datetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'datetime': APIHelper.when_defined(APIHelper.HttpDateTime, datetime)
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

    def send_rfc_3339_date_time(self,
                                datetime):
        """Does a POST request to /form/rfc3339datetime.

        TODO: type endpoint description here.

        Args:
            datetime (datetime): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(datetime=datetime)

        # Prepare query URL
        _url_path = '/form/rfc3339datetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'datetime': APIHelper.when_defined(APIHelper.RFC3339DateTime, datetime)
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

    def send_unix_date_time_array(self,
                                  datetimes):
        """Does a POST request to /form/unixdatetime.

        TODO: type endpoint description here.

        Args:
            datetimes (list of datetime): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(datetimes=datetimes)

        # Prepare query URL
        _url_path = '/form/unixdatetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'datetimes': [APIHelper.when_defined(APIHelper.UnixDateTime, element) for element in datetimes]
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

    def send_rfc_1123_date_time_array(self,
                                      datetimes):
        """Does a POST request to /form/rfc1123datetime.

        TODO: type endpoint description here.

        Args:
            datetimes (list of datetime): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(datetimes=datetimes)

        # Prepare query URL
        _url_path = '/form/rfc1123datetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'datetimes': [APIHelper.when_defined(APIHelper.HttpDateTime, element) for element in datetimes]
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

    def send_long(self,
                  value):
        """Does a POST request to /form/number.

        TODO: type endpoint description here.

        Args:
            value (long|int): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(value=value)

        # Prepare query URL
        _url_path = '/form/number'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
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

    def send_integer_array(self,
                           integers):
        """Does a POST request to /form/number.

        TODO: type endpoint description here.

        Args:
            integers (list of int): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(integers=integers)

        # Prepare query URL
        _url_path = '/form/number'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'integers': integers
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

    def send_string_array(self,
                          strings):
        """Does a POST request to /form/string.

        TODO: type endpoint description here.

        Args:
            strings (list of string): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(strings=strings)

        # Prepare query URL
        _url_path = '/form/string'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'strings': strings
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

    def allow_dynamic_form_fields(self,
                                  name,
                                  _optional_form_parameters=None):
        """Does a POST request to /form/allowDynamicFormFields.

        TODO: type endpoint description here.

        Args:
            name (string): TODO: type description here.
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

        # Validate required parameters
        self.validate_parameters(name=name)

        # Prepare query URL
        _url_path = '/form/allowDynamicFormFields'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'name': name
        }
        if _form_parameters is not None and _optional_form_parameters is not None:
            _form_parameters.update(
                APIHelper.form_encode_parameters(_optional_form_parameters,
                                                 self.config.array_serialization)
            )
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_model(self,
                   model):
        """Does a POST request to /form/model.

        TODO: type endpoint description here.

        Args:
            model (Employee): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(model=model)

        # Prepare query URL
        _url_path = '/form/model'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'model': model
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_model_array(self,
                         models):
        """Does a POST request to /form/model.

        TODO: type endpoint description here.

        Args:
            models (list of Employee): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(models=models)

        # Prepare query URL
        _url_path = '/form/model'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'models': models
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_file(self,
                  file):
        """Does a POST request to /form/file.

        TODO: type endpoint description here.

        Args:
            file (string): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(file=file)

        # Prepare query URL
        _url_path = '/form/file'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare files
        _files = {
            'file': file
        }

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, files=_files)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_multiple_files(self,
                            file,
                            file_1):
        """Does a POST request to /form/multipleFiles.

        TODO: type endpoint description here.

        Args:
            file (string): TODO: type description here.
            file_1 (string): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(file=file,
                                 file_1=file_1)

        # Prepare query URL
        _url_path = '/form/multipleFiles'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare files
        _files = {
            'file': file,
            'file1': file_1
        }

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, files=_files)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_string(self,
                    value):
        """Does a POST request to /form/string.

        TODO: type endpoint description here.

        Args:
            value (string): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(value=value)

        # Prepare query URL
        _url_path = '/form/string'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
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

    def send_rfc_3339_date_time_array(self,
                                      datetimes):
        """Does a POST request to /form/rfc3339datetime.

        TODO: type endpoint description here.

        Args:
            datetimes (list of datetime): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(datetimes=datetimes)

        # Prepare query URL
        _url_path = '/form/rfc3339datetime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'datetimes': [APIHelper.when_defined(APIHelper.RFC3339DateTime, element) for element in datetimes]
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

                    file -- string -- TODO: type description here.
                    integers -- list of int -- TODO: type description here.
                    models -- list of Employee -- TODO: type description
                        here.
                    strings -- list of string -- TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(file=options.get("file"),
                                 integers=options.get("integers"),
                                 models=options.get("models"),
                                 strings=options.get("strings"))

        # Prepare query URL
        _url_path = '/form/mixed'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare files
        _files = {
            'file': options.get('file', None)
        }

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'integers': options.get('integers', None),
            'models': options.get('models', None),
            'strings': options.get('strings', None)
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters, files=_files)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def update_model_with_form(self,
                               model):
        """Does a PUT request to /form/updateModel.

        TODO: type endpoint description here.

        Args:
            model (Employee): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(model=model)

        # Prepare query URL
        _url_path = '/form/updateModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'model': model
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.put(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_delete_form_1(self,
                           model):
        """Does a DELETE request to /form/deleteForm1.

        TODO: type endpoint description here.

        Args:
            model (Employee): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(model=model)

        # Prepare query URL
        _url_path = '/form/deleteForm1'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'model': model
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.delete(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_delete_form_with_model_array(self,
                                          models):
        """Does a DELETE request to /form/deleteForm1.

        TODO: type endpoint description here.

        Args:
            models (list of Employee): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(models=models)

        # Prepare query URL
        _url_path = '/form/deleteForm1'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'models': models
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.delete(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def update_model_array_with_form(self,
                                     models):
        """Does a PUT request to /form/updateModel.

        TODO: type endpoint description here.

        Args:
            models (list of Employee): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(models=models)

        # Prepare query URL
        _url_path = '/form/updateModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'models': models
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.put(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def update_string_with_form(self,
                                value):
        """Does a PUT request to /form/updateString.

        TODO: type endpoint description here.

        Args:
            value (string): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(value=value)

        # Prepare query URL
        _url_path = '/form/updateString'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'value': value
        }

        # Prepare and execute request
        _request = self.config.http_client.put(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def update_string_array_with_form(self,
                                      strings):
        """Does a PUT request to /form/updateString.

        TODO: type endpoint description here.

        Args:
            strings (list of string): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(strings=strings)

        # Prepare query URL
        _url_path = '/form/updateString'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'strings': strings
        }

        # Prepare and execute request
        _request = self.config.http_client.put(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_integer_enum_array(self,
                                suites):
        """Does a POST request to /form/integerenum.

        TODO: type endpoint description here.

        Args:
            suites (list of SuiteCode): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(suites=suites)

        # Prepare query URL
        _url_path = '/form/integerenum'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'suites': suites
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

    def send_string_enum_array(self,
                               days):
        """Does a POST request to /form/stringenum.

        TODO: type endpoint description here.

        Args:
            days (list of Days): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(days=days)

        # Prepare query URL
        _url_path = '/form/stringenum'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_parameters = {
            'array': True
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

        # Prepare form parameters
        _form_parameters = {
            'days': days
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

    def send_string_in_form_with_new_line(self,
                                          body):
        """Does a POST request to /form/stringEncoding.

        TODO: type endpoint description here.

        Args:
            body (TestNstringEncoding): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/stringEncoding'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_string_in_form_with_r(self,
                                   body):
        """Does a POST request to /form/stringEncoding.

        TODO: type endpoint description here.

        Args:
            body (TestRstringEncoding): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/stringEncoding'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_string_in_form_with_r_n(self,
                                     body):
        """Does a POST request to /form/stringEncoding.

        TODO: type endpoint description here.

        Args:
            body (TestRNstringEncoding): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/stringEncoding'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_optional_unix_date_time_in_body(self,
                                             date_time=None):
        """Does a POST request to /form/optionalUnixTimeStamp.

        TODO: type endpoint description here.

        Args:
            date_time (datetime, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/form/optionalUnixTimeStamp'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'dateTime': APIHelper.when_defined(APIHelper.UnixDateTime, date_time)
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

    def send_optional_rfc_1123_in_body(self,
                                       body):
        """Does a POST request to /form/optionlRfc1123.

        TODO: type endpoint description here.

        Args:
            body (datetime): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/optionlRfc1123'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': APIHelper.when_defined(APIHelper.HttpDateTime, body)
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

    def send_datetime_optional_in_endpoint(self,
                                           body=None):
        """Does a POST request to /form/optionalDateTime.

        TODO: type endpoint description here.

        Args:
            body (datetime, optional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Prepare query URL
        _url_path = '/form/optionalDateTime'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': APIHelper.when_defined(APIHelper.RFC3339DateTime, body)
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

    def send_optional_unix_time_stamp_in_model_body(self,
                                                    date_time):
        """Does a POST request to /form/optionalUnixDateTimeInModel.

        TODO: type endpoint description here.

        Args:
            date_time (UnixDateTime): TODO: type description here.

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
        _url_path = '/form/optionalUnixDateTimeInModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'dateTime': date_time
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_optional_unix_time_stamp_in_nested_model_body(self,
                                                           date_time):
        """Does a POST request to /form/optionalUnixTimeStampInNestedModel.

        TODO: type endpoint description here.

        Args:
            date_time (SendUnixDateTime): TODO: type description here.

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
        _url_path = '/form/optionalUnixTimeStampInNestedModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'dateTime': date_time
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_rfc_1123_date_time_in_nested_model(self,
                                                body):
        """Does a POST request to /form/rfc1123InNestedModel.

        TODO: type endpoint description here.

        Args:
            body (SendRfc1123DateTime): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/rfc1123InNestedModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_rfc_1123_date_time_in_model(self,
                                         date_time):
        """Does a POST request to /form/OptionalRfc1123InModel.

        TODO: type endpoint description here.

        Args:
            date_time (ModelWithOptionalRfc1123DateTime): TODO: type
                description here.

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
        _url_path = '/form/OptionalRfc1123InModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'dateTime': date_time
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_optional_datetime_in_model(self,
                                        body):
        """Does a POST request to /form/optionalDateTimeInBody.

        TODO: type endpoint description here.

        Args:
            body (ModelWithOptionalRfc3339DateTime): TODO: type description
                here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/optionalDateTimeInBody'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_rfc_339_date_time_in_nested_models(self,
                                                body):
        """Does a POST request to /form/dateTimeInNestedModel.

        TODO: type endpoint description here.

        Args:
            body (SendRfc339DateTime): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/dateTimeInNestedModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def uuid_as_optional(self,
                         body):
        """Does a POST request to /form/optionalUUIDInModel.

        TODO: type endpoint description here.

        Args:
            body (UuidAsOptional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/optionalUUIDInModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def boolean_as_optional(self,
                            body):
        """Does a POST request to /form/optionalBooleanInModel.

        TODO: type endpoint description here.

        Args:
            body (BooleanAsOptional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/optionalBooleanInModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def date_as_optional(self,
                         body):
        """Does a POST request to /form/optionalDateInModel.

        TODO: type endpoint description here.

        Args:
            body (DateAsOptional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/optionalDateInModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def dynamic_as_optional(self,
                            body):
        """Does a POST request to /form/optionalDynamicInModel.

        TODO: type endpoint description here.

        Args:
            body (DynamicAsOptional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/optionalDynamicInModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def string_as_optional(self,
                           body):
        """Does a POST request to /form/optionalStringInModel.

        TODO: type endpoint description here.

        Args:
            body (StringAsOptional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/optionalStringInModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def precision_as_optional(self,
                              body):
        """Does a POST request to /form/optionalPrecisionInModel.

        TODO: type endpoint description here.

        Args:
            body (PrecisionAsOptional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/optionalPrecisionInModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def long_as_optional(self,
                         body):
        """Does a POST request to /form/optionalLongInModel.

        TODO: type endpoint description here.

        Args:
            body (LongAsOptional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/optionalLongInModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)

    def send_number_as_optional(self,
                                body):
        """Does a POST request to /form/optionalNumberInModel.

        TODO: type endpoint description here.

        Args:
            body (NumberAsOptional): TODO: type description here.

        Returns:
            ServerResponse: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        # Validate required parameters
        self.validate_parameters(body=body)

        # Prepare query URL
        _url_path = '/form/optionalNumberInModel'
        _query_builder = self.config.get_base_uri()
        _query_builder += _url_path
        _query_url = APIHelper.clean_url(_query_builder)

        # Prepare headers
        _headers = {
            'accept': 'application/json'
        }

        # Prepare form parameters
        _form_parameters = {
            'body': body
        }
        _form_parameters = APIHelper.form_encode_parameters(
            _form_parameters,
            self.config.array_serialization
        )

        # Prepare and execute request
        _request = self.config.http_client.post(_query_url, headers=_headers, parameters=_form_parameters)
        _context = self.execute_request(_request)

        # Endpoint and global error handling using HTTP status codes.
        if _context.response.status_code == 404:
            return None
        self.validate_response(_context)

        # Return appropriate type
        return APIHelper.json_deserialize(_context.response.raw_body, ServerResponse.from_dictionary)
