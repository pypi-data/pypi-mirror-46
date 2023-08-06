# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.response_data


class Complex5(object):

    """Implementation of the 'complex5' model.

    TODO: type model description here.

    Attributes:
        response_data (ResponseData): TODO: type description here.
        response_details (string): TODO: type description here.
        response_status (int): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "response_data": 'responseData',
        "response_status": 'responseStatus',
        "response_details": 'responseDetails'
    }

    def __init__(self,
                 response_data=None,
                 response_status=None,
                 response_details=None,
                 additional_properties={}):
        """Constructor for the Complex5 class"""

        # Initialize members of the class
        self.response_data = response_data
        self.response_details = response_details
        self.response_status = response_status

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
        response_data = tester.models.response_data.ResponseData.from_dictionary(dictionary.get('responseData')) if dictionary.get('responseData') else None
        response_status = dictionary.get('responseStatus')
        response_details = dictionary.get('responseDetails')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(response_data,
                   response_status,
                   response_details,
                   dictionary)
