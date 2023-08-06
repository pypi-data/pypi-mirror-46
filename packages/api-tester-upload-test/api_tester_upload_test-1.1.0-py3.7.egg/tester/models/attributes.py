# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class Attributes(object):

    """Implementation of the 'Attributes' model.

    TODO: type model description here.

    Attributes:
        exclusive_maximum (bool): TODO: type description here.
        exclusive_minimum (bool): TODO: type description here.
        id (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "exclusive_maximum": 'exclusiveMaximum',
        "exclusive_minimum": 'exclusiveMinimum',
        "id": 'id'
    }

    def __init__(self,
                 exclusive_maximum=None,
                 exclusive_minimum=None,
                 id=None,
                 additional_properties={}):
        """Constructor for the Attributes class"""

        # Initialize members of the class
        self.exclusive_maximum = exclusive_maximum
        self.exclusive_minimum = exclusive_minimum
        self.id = id

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
        exclusive_maximum = dictionary.get('exclusiveMaximum')
        exclusive_minimum = dictionary.get('exclusiveMinimum')
        id = dictionary.get('id')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(exclusive_maximum,
                   exclusive_minimum,
                   id,
                   dictionary)
