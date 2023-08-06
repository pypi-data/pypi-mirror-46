# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.model_with_optional_rfc_3339_date_time


class SendRfc339DateTime(object):

    """Implementation of the 'Send rfc339 dateTime' model.

    TODO: type model description here.

    Attributes:
        date_time (ModelWithOptionalRfc3339DateTime): TODO: type description
            here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "date_time": 'dateTime'
    }

    def __init__(self,
                 date_time=None,
                 additional_properties={}):
        """Constructor for the SendRfc339DateTime class"""

        # Initialize members of the class
        self.date_time = date_time

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
        date_time = tester.models.model_with_optional_rfc_3339_date_time.ModelWithOptionalRfc3339DateTime.from_dictionary(dictionary.get('dateTime')) if dictionary.get('dateTime') else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(date_time,
                   dictionary)
