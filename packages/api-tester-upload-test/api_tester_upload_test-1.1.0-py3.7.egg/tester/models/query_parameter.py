# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class QueryParameter(object):

    """Implementation of the 'QueryParameter' model.

    Query parameter key value pair echoed back from the server.

    Attributes:
        key (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "key": 'key'
    }

    def __init__(self,
                 key=None,
                 additional_properties={}):
        """Constructor for the QueryParameter class"""

        # Initialize members of the class
        self.key = key

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
        key = dictionary.get('key')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(key,
                   dictionary)
