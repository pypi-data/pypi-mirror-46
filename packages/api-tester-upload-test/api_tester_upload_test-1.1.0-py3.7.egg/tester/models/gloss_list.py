# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.gloss_entry


class GlossList(object):

    """Implementation of the 'GlossList' model.

    TODO: type model description here.

    Attributes:
        gloss_entry (GlossEntry): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "gloss_entry": 'GlossEntry'
    }

    def __init__(self,
                 gloss_entry=None,
                 additional_properties={}):
        """Constructor for the GlossList class"""

        # Initialize members of the class
        self.gloss_entry = gloss_entry

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
        gloss_entry = tester.models.gloss_entry.GlossEntry.from_dictionary(dictionary.get('GlossEntry')) if dictionary.get('GlossEntry') else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(gloss_entry,
                   dictionary)
