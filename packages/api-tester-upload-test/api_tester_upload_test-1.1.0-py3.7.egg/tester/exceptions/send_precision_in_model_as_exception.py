# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""

from tester.api_helper import APIHelper
import tester.exceptions.api_exception
import tester.models.add_precision_in_exception


class SendPrecisionInModelAsException(tester.exceptions.api_exception.APIException):
    def __init__(self, reason, context):
        """Constructor for the SendPrecisionInModelAsException class

        Args:
            reason (string): The reason (or error message) for the Exception
                to be raised.
            context (HttpContext):  The HttpContext of the API call.

        """
        super(SendPrecisionInModelAsException, self).__init__(reason, context)
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
        self.body = tester.models.add_precision_in_exception.AddPrecisionInException.from_dictionary(dictionary.get('body')) if dictionary.get('body') else None
