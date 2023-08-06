# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""
import tester.models.glossary


class Complex2(object):

    """Implementation of the 'complex2' model.

    TODO: type model description here.

    Attributes:
        glossary (Glossary): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "glossary": 'glossary'
    }

    def __init__(self,
                 glossary=None,
                 additional_properties={}):
        """Constructor for the Complex2 class"""

        # Initialize members of the class
        self.glossary = glossary

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
        glossary = tester.models.glossary.Glossary.from_dictionary(dictionary.get('glossary')) if dictionary.get('glossary') else None

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(glossary,
                   dictionary)
