# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class RedirectSettings(object):

    """Implementation of the 'RedirectSettings' model.

    TODO: type model description here.

    Attributes:
        redirect_mode (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "redirect_mode": 'redirectMode'
    }

    def __init__(self,
                 redirect_mode=None,
                 additional_properties={}):
        """Constructor for the RedirectSettings class"""

        # Initialize members of the class
        self.redirect_mode = redirect_mode

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
        redirect_mode = dictionary.get('redirectMode')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(redirect_mode,
                   dictionary)
