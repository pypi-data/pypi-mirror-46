# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class GlossDef(object):

    """Implementation of the 'GlossDef' model.

    TODO: type model description here.

    Attributes:
        para (string): TODO: type description here.
        gloss_see_also (list of string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "gloss_see_also": 'GlossSeeAlso',
        "para": 'para'
    }

    def __init__(self,
                 gloss_see_also=None,
                 para=None,
                 additional_properties={}):
        """Constructor for the GlossDef class"""

        # Initialize members of the class
        self.para = para
        self.gloss_see_also = gloss_see_also

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
        gloss_see_also = dictionary.get('GlossSeeAlso')
        para = dictionary.get('para')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(gloss_see_also,
                   para,
                   dictionary)
