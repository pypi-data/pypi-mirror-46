# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""

import dateutil.parser
from tester.api_helper import APIHelper
import tester.exceptions.api_exception


class ExceptionWithDateException(tester.exceptions.api_exception.APIException):
    def __init__(self, reason, context):
        """Constructor for the ExceptionWithDateException class

        Args:
            reason (string): The reason (or error message) for the Exception
                to be raised.
            context (HttpContext):  The HttpContext of the API call.

        """
        super(ExceptionWithDateException, self).__init__(reason, context)
        dictionary = APIHelper.json_deserialize(self.context.response.raw_body)
        if isinstance(dictionary, dict):
            self.unbox(dictionary)

    def unbox(self, dictionary):
        """Populates the properties of this object by extracting them from a dictionary.

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        """
        self.value = dateutil.parser.parse(dictionary.get('value')).date() if dictionary.get('value') else None
        self.value_1 = dateutil.parser.parse(dictionary.get('value1')).date() if dictionary.get('value1') else None
