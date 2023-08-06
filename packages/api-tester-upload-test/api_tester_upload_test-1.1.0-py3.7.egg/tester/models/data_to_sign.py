# -*- coding: utf-8 -*-

"""
tester

This file was automatically generated for Stamplay by APIMATIC v2.0 (
 https://apimatic.io ).
"""


class DataToSign(object):

    """Implementation of the 'DataToSign' model.

    TODO: type model description here.

    Attributes:
        file_name (string): TODO: type description here.
        convert_to_pdf (bool): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "convert_to_pdf": 'convertToPDF',
        "file_name": 'fileName'
    }

    def __init__(self,
                 convert_to_pdf=None,
                 file_name=None,
                 additional_properties={}):
        """Constructor for the DataToSign class"""

        # Initialize members of the class
        self.file_name = file_name
        self.convert_to_pdf = convert_to_pdf

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
        convert_to_pdf = dictionary.get('convertToPDF')
        file_name = dictionary.get('fileName')

        # Clean out expected properties from dictionary
        for key in cls._names.values():
            if key in dictionary:
                del dictionary[key]

        # Return an object of this model
        return cls(convert_to_pdf,
                   file_name,
                   dictionary)
