# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class Styling(object):

    """Implementation of the 'Styling' model.

    TODO: type model description here.

    Attributes:
        color_theme (string): TODO: type description here.
        spinner (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "color_theme": 'colorTheme',
        "spinner": 'spinner'
    }

    def __init__(self,
                 color_theme=None,
                 spinner=None,
                 additional_properties={}):
        """Constructor for the Styling class"""

        # Initialize members of the class
        self.color_theme = color_theme
        self.spinner = spinner

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
        color_theme = dictionary.get('colorTheme')
        spinner = dictionary.get('spinner')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(color_theme,
                   spinner,
                   dictionary)
