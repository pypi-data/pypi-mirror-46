# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class BooleanAsOptional(object):

    """Implementation of the 'Boolean as optional' model.

    TODO: type model description here.

    Attributes:
        boolean (bool): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "boolean": 'boolean'
    }

    def __init__(self,
                 boolean=None,
                 additional_properties={}):
        """Constructor for the BooleanAsOptional class"""

        # Initialize members of the class
        self.boolean = boolean

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
        boolean = dictionary.get('boolean')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(boolean,
                   dictionary)
