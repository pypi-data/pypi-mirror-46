# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class Validate(object):

    """Implementation of the 'validate' model.

    TODO: type model description here.

    Attributes:
        field (string): TODO: type description here.
        name (string): TODO: type description here.
        address (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "field": 'field',
        "name": 'name',
        "address": 'address'
    }

    def __init__(self,
                 field=None,
                 name=None,
                 address=None,
                 additional_properties={}):
        """Constructor for the Validate class"""

        # Initialize members of the class
        self.field = field
        self.name = name
        self.address = address

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
        field = dictionary.get('field')
        name = dictionary.get('name')
        address = dictionary.get('address')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(field,
                   name,
                   address,
                   dictionary)
