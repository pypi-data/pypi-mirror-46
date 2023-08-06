# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.gloss_list


class GlossDiv(object):

    """Implementation of the 'GlossDiv' model.

    TODO: type model description here.

    Attributes:
        title (string): TODO: type description here.
        gloss_list (GlossList): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "gloss_list": 'GlossList',
        "title": 'title'
    }

    def __init__(self,
                 gloss_list=None,
                 title=None,
                 additional_properties={}):
        """Constructor for the GlossDiv class"""

        # Initialize members of the class
        self.title = title
        self.gloss_list = gloss_list

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
        gloss_list = tester.models.gloss_list.GlossList.from_dictionary(dictionary.get('GlossList')) if dictionary.get('GlossList') else None
        title = dictionary.get('title')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(gloss_list,
                   title,
                   dictionary)
