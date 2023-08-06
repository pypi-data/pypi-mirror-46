# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
from tester.api_helper import APIHelper


class AddRfc1123DatetimeInGlobalException(object):

    """Implementation of the 'Add rfc1123 datetime in global exception' model.

    TODO: type model description here.

    Attributes:
        date_time (datetime): TODO: type description here.
        date_time_1 (datetime): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "date_time": 'dateTime',
        "date_time_1": 'dateTime1'
    }

    def __init__(self,
                 date_time=None,
                 date_time_1=None,
                 additional_properties={}):
        """Constructor for the AddRfc1123DatetimeInGlobalException class"""

        # Initialize members of the class
        self.date_time = APIHelper.HttpDateTime(date_time) if date_time else None
        self.date_time_1 = APIHelper.HttpDateTime(date_time_1) if date_time_1 else None

        # Add additional model properties to the instance
        self.additional_properties = additional_properties

    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object
            as obtained from the deserialization of the server's response. The
            keys MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        date_time = APIHelper.HttpDateTime.from_value(dictionary.get("dateTime")).datetime if dictionary.get("dateTime") else None
        date_time_1 = APIHelper.HttpDateTime.from_value(dictionary.get("dateTime1")).datetime if dictionary.get("dateTime1") else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(date_time,
                   date_time_1,
                   dictionary)
