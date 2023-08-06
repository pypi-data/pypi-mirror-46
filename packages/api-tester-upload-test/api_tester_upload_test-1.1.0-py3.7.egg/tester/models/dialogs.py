# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.before


class Dialogs(object):

    """Implementation of the 'Dialogs' model.

    TODO: type model description here.

    Attributes:
        before (Before): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "before": 'before'
    }

    def __init__(self,
                 before=None,
                 additional_properties={}):
        """Constructor for the Dialogs class"""

        # Initialize members of the class
        self.before = before

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
        before = tester.models.before.Before.from_dictionary(dictionary.get('before')) if dictionary.get('before') else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(before,
                   dictionary)
