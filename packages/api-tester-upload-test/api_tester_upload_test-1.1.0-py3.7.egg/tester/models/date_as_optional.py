# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import dateutil.parser


class DateAsOptional(object):

    """Implementation of the 'date as optional' model.

    TODO: type model description here.

    Attributes:
        date (date): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "date": 'date'
    }

    def __init__(self,
                 date=None,
                 additional_properties={}):
        """Constructor for the DateAsOptional class"""

        # Initialize members of the class
        self.date = date

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
        date = dateutil.parser.parse(dictionary.get('date')).date() if dictionary.get('date') else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(date,
                   dictionary)
