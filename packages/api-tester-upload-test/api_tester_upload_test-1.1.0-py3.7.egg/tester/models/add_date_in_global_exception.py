# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import dateutil.parser


class AddDateInGlobalException(object):

    """Implementation of the 'Add date in global exception' model.

    TODO: type model description here.

    Attributes:
        value (date): TODO: type description here.
        value_1 (date): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "value": 'value',
        "value_1": 'value1'
    }

    def __init__(self,
                 value=None,
                 value_1=None,
                 additional_properties={}):
        """Constructor for the AddDateInGlobalException class"""

        # Initialize members of the class
        self.value = value
        self.value_1 = value_1

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
        value = dateutil.parser.parse(dictionary.get('value')).date() if dictionary.get('value') else None
        value_1 = dateutil.parser.parse(dictionary.get('value1')).date() if dictionary.get('value1') else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(value,
                   value_1,
                   dictionary)
