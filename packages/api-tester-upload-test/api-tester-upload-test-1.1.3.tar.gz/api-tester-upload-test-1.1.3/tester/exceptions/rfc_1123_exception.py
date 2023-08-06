# -*- coding: utf-8 -*-

"""
    tester

    This file was automatically generated for Stamplay by APIMATIC v2.0 ( https://apimatic.io ).
"""

from tester.api_helper import APIHelper
import tester.exceptions.api_exception

class Rfc1123Exception(tester.exceptions.api_exception.APIException):
    def __init__(self, reason, context):
        """Constructor for the Rfc1123Exception class

        Args:
            reason (string): The reason (or error message) for the Exception
                to be raised.
            context (HttpContext):  The HttpContext of the API call.

        """
        super(Rfc1123Exception, self).__init__(reason, context)
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
        self.date_time = APIHelper.HttpDateTime.from_value(dictionary.get("dateTime")).datetime if dictionary.get("dateTime") else None
        self.date_time_1 = APIHelper.HttpDateTime.from_value(dictionary.get("dateTime1")).datetime if dictionary.get("dateTime1") else None
